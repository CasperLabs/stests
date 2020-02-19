import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.utils import factory
from stests.core.cache import NetworkIdentifier
from stests.core.domain import BlockStatus



# Queue to which messages will be dispatched.
_QUEUE = "monitoring"


@dramatiq.actor(queue_name=f"{_QUEUE}.on_block_finalized")
def on_block_finalized(network_id: NetworkIdentifier, bhash: str):   
    """Event: raised whenever a block is finalized.
    
    """
    # Get block info.
    block = clx.get_block(network_id, bhash)

    # Set block status.
    block.status = BlockStatus.FINALIZED

    # Encache.
    cache.set_block(network_id, block)  

    # Enqueue deploys.
    for dhash in clx.get_block_deploys(network_id, bhash):
        on_deploy_finalized.send(network_id, bhash, dhash)


@dramatiq.actor(queue_name=f"{_QUEUE}.on_deploy_finalized")
def on_deploy_finalized(network_id: NetworkIdentifier, bhash: str, dhash: str):   
    """Processes a finalized deploy.
    
    """
    print(f"TODO on_deploy_finalized : {network_id.name} : {bhash} : {dhash}")
