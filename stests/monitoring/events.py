import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.utils import factory
from stests.core.domain import DeployStatus
from stests.core.domain import NetworkIdentifier
from stests.core.domain import NodeIdentifier
from stests.core.utils import logger
from stests.orchestration.actors import on_step_deploy_finalized


# Queue to which messages will be dispatched.
_QUEUE = "monitoring"


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
    _, encached = cache.monitoring.set_block(block)  
    if not encached:
        return
    
    logger.log(f"PYCLX :: processing finalized block: bhash={bhash}")

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
    _, encached = cache.monitoring.set_deploy(deploy)
    if not encached:
        return

    # Pull run deploy - escape if none found.
    deploy = cache.state.get_deploy(dhash)
    if not deploy:
        return
    logger.log(f"PYCLX :: run deploy finalized: dhash={dhash} :: bhash={bhash}")

    # Update deploy.
    deploy.update_on_finalization(bhash, finalization_ts)
    cache.state.set_deploy(deploy)

    # Increment deploy counts.
    ctx = cache.orchestration.get_context(deploy.network, deploy.run_index, deploy.run_type)
    cache.orchestration.increment_deploy_counts(ctx)

    # Update transfers.
    transfer = cache.state.get_transfer(dhash)
    if transfer:
        transfer.update_on_completion()
        cache.state.set_transfer(transfer)
    
    # Signal to orchestrator.
    on_step_deploy_finalized.send(ctx, bhash, dhash)
