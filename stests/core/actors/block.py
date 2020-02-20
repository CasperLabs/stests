import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.utils import factory
from stests.core.domain import BlockStatus
from stests.core.domain import DeployStatus
from stests.core.domain import NetworkIdentifier

from stests.core.actors.correlation import do_correlate_finalized_deploy



# Queue to which messages will be dispatched.
_QUEUE = "monitoring"


@dramatiq.actor(queue_name=_QUEUE)
def on_block_finalized(network_id: NetworkIdentifier, block_hash: str):   
    """Event: raised whenever a block is finalized.

    :param network_id: Identifier of network upon which a block has been finalized.
    :param block_hash: Hash of finalized block.

    """
    # Get block info.
    block = clx.get_block(network_id, block_hash)

    # Set block status.
    block.status = BlockStatus.FINALIZED

    # Encache & escape if another stream handler has already processed this block.
    _, already_processed = cache.set_network_block(network_id, block)  
    if not already_processed:
        return

    # Enqueue deploys.
    for deploy_hash in clx.get_block_deploys(network_id, block_hash):        
        on_deploy_finalized.send(network_id, block_hash, deploy_hash, block.timestamp)


@dramatiq.actor(queue_name=_QUEUE)
def on_deploy_finalized(network_id: NetworkIdentifier, block_hash: str, deploy_hash: str, ts_finalized: int):   
    """Event: raised whenever a deploy is finalized.
    
    :param network_id: Identifier of network upon which a block has been finalized.
    :param block_hash: Hash of finalized block.
    :param deploy_hash: Hash of finalized deploy.
    :param ts_finalized: Moment in time when finalization occurred.

    """
    # Set deploy info.
    deploy = factory.create_deploy(network_id, block_hash, deploy_hash, DeployStatus.FINALIZED)    

    # Encache & escape if another stream handler has already processed this deploy.
    _, already_processed = cache.set_network_deploy(network_id, deploy)
    if not already_processed:
        return

    # Enqueue for generators.
    do_correlate_finalized_deploy.send(block_hash, deploy_hash, ts_finalized)
