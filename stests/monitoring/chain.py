from datetime import datetime

import dramatiq
from dramatiq.middleware import TimeLimitExceeded

from stests.core import cache
from stests.core import clx
from stests.core.utils import factory
from stests.core.domain import DeployStatus
from stests.core.domain import NetworkIdentifier
from stests.core.domain import NodeIdentifier
from stests.core.utils import logger
from stests.monitoring.correlator import correlate_finalized_deploy



# Queue to which messages will be dispatched.
_QUEUE = "monitoring"



@dramatiq.actor(queue_name=_QUEUE)
def launch_stream_monitors():
    """Launches network stream endpoint monitors.
    
    """
    for network in cache.get_networks():
        network_id = factory.create_network_id(network.name)
        for idx, node in enumerate(cache.get_nodes_operational(network)):
            node_id = factory.create_node_id(network_id, node.index)
            do_monitor_blocks.send_with_options(args=(node_id, ), delay=idx * 500)
            break


@dramatiq.actor(queue_name=_QUEUE)
def do_monitor_blocks(node_id: NodeIdentifier):   
    """Wires upto chain event streaming.
    
    """
    # Callback,
    def _on_block_finalized(_, bhash):
        on_finalized_block.send(node_id, bhash)
    
    # Stream events and re-queue when actor timeout occurs.
    try:
        clx.stream_events(node_id, on_block_finalized=_on_block_finalized)
    except TimeLimitExceeded:
        do_monitor_blocks.send(node_id)


@dramatiq.actor(queue_name=_QUEUE)
def on_finalized_block(node_id: NodeIdentifier, bhash: str):   
    """Event: raised whenever a block is finalized.

    :param node_id: Identifier of node from which block was streamed.
    :param bhash: Hash of finalized block.

    """
    # Query block info & set block status accordingly.
    block = clx.get_block(node_id.network, bhash)
    block.update_on_finalization()

    # Encache - skip duplicates.
    _, encached = cache.set_block(block)  
    if not encached:
        return

    # Enqueue finalized deploys.
    for dhash in clx.get_deploys(node_id.network, bhash):  
        on_finalized_deploy.send(node_id.network, bhash, dhash, block.timestamp)


@dramatiq.actor(queue_name=_QUEUE)
def on_finalized_deploy(network_id: NetworkIdentifier, bhash: str, dhash: str, finalization_ts: float):   
    """Event: raised whenever a deploy is finalized.
    
    :param network_id: Identifier of network upon which a block has been finalized.
    :param bhash: Hash of finalized block.
    :param dhash: Hash of finalized deploy.
    :param finalization_ts: Moment in time when finalization occurred.

    """
    # Set network deploy.
    deploy = factory.create_deploy(network_id, bhash, dhash, DeployStatus.FINALIZED)

    # Encache - skip duplicates.
    _, encached = cache.set_deploy(deploy)
    if not encached:
        return

    # Pull run deploy.
    deploy = cache.get_run_deploy(dhash)
    if not deploy:
        logger.log_warning(f"Could not find finalized run deploy information: {bhash} : {dhash}")
        return

    # Update run deploy.
    deploy.update_on_finalization(bhash, finalization_ts)
    cache.set_run_deploy(deploy)

    # Increment run step deploy count.
    ctx = cache.get_context(deploy.network, deploy.run, deploy.run_type)
    cache.increment_step_deploy_count(ctx)

    # Update run transfer.
    transfer = cache.get_run_transfer(dhash)
    if transfer:
        transfer.update_on_completion()
        cache.set_run_transfer(transfer)
    
    # Signal to workload generator correlator.
    correlate_finalized_deploy.send(ctx, dhash)
