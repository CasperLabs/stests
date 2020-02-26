import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.utils import factory
from stests.core.domain import BlockStatus
from stests.core.domain import Deploy
from stests.core.domain import DeployStatus
from stests.core.domain import NetworkIdentifier
from stests.core.domain import NodeIdentifier
from stests.core.domain import Transfer
from stests.core.domain import TransferStatus
from stests.core.utils import logger
from stests.monitoring.correlator import correlate_finalized_deploy



# Queue to which messages will be dispatched.
_QUEUE = "monitoring"


@dramatiq.actor(queue_name=_QUEUE)
def do_monitor_blocks(node_id: NodeIdentifier):   
    """Wires upto chain event streaming.
    
    """
    network_id = node_id.network
    clx.stream_events(
        node_id.network,
        on_block_finalized=lambda bhash: on_finalized_block.send(network_id, bhash)
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_finalized_block(network_id: NetworkIdentifier, bhash: str):   
    """Event: raised whenever a block is finalized.

    :param network_id: Identifier of network upon which a block has been finalized.
    :param bhash: Hash of finalized block.

    """
    # Query block info & set block status accordingly.
    block = clx.get_block(network_id, bhash)
    block.status = BlockStatus.FINALIZED

    # Encache - skip duplicates.
    _, encached = cache.set_network_block(block)  
    if not encached:
        return

    # Enqueue finalized deploys.
    for dhash in clx.get_block_deploys(network_id, bhash):  
        on_finalized_deploy.send(network_id, bhash, dhash, block.timestamp)


@dramatiq.actor(queue_name=_QUEUE)
def on_finalized_deploy(network_id: NetworkIdentifier, bhash: str, dhash: str, ts_finalized: int):   
    """Event: raised whenever a deploy is finalized.
    
    :param network_id: Identifier of network upon which a block has been finalized.
    :param bhash: Hash of finalized block.
    :param dhash: Hash of finalized deploy.
    :param ts_finalized: Moment in time when finalization occurred.

    """
    # Set network deploy.
    deploy = factory.create_deploy(network_id, bhash, dhash, DeployStatus.FINALIZED)    

    # Encache - skip duplicates.
    _, encached = cache.set_network_deploy(deploy)
    if not encached:
        return

    # Update run deploy.
    deploy = cache.get_run_deploy(dhash)
    if not deploy:
        logger.log_warning(f"Could not find finalized run deploy information: {bhash} : {dhash}")
        return
    deploy.block_hash = bhash
    deploy.status = DeployStatus.FINALIZED
    deploy.ts_finalized = ts_finalized
    cache.set_run_deploy(deploy)

    # Update run step deploy.
    ctx = cache.get_run_context(deploy.network, deploy.run, deploy.run_type)
    cache.set_run_step_deploy(ctx, deploy)

    # Update transfer.
    transfer = cache.get_run_transfer(dhash)
    if transfer:
        transfer.status = TransferStatus.COMPLETE
        cache.set_run_transfer(transfer)
    
    # Signal downstream to workload generator.
    correlate_finalized_deploy.send(ctx, dhash)
