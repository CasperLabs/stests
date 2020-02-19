import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.utils import factory
from stests.core.domain import BlockStatus
from stests.core.domain import NetworkIdentifier



# Queue to which messages will be dispatched.
_QUEUE = "monitoring"


@dramatiq.actor(queue_name=f"{_QUEUE}.on_block_finalized")
def on_block_finalized(network_id: NetworkIdentifier, bhash: str):   
    """Event: raised whenever a block is finalized.

    :param network_id: Identifier of network upon which a block has been finalized.
    :param bhash: Hash of finalized block.

    """
    # Get block info.
    block = clx.get_block(network_id, bhash)

    # Set block status.
    block.status = BlockStatus.FINALIZED

    # Encache.
    cache.set_network_block(network_id, block)  

    # Enqueue deploys.
    for dhash in clx.get_block_deploys(network_id, bhash):
        on_deploy_finalized.send(network_id, bhash, dhash)


@dramatiq.actor(queue_name=f"{_QUEUE}.on_deploy_finalized")
def on_deploy_finalized(network_id: NetworkIdentifier, bhash: str, dhash: str):   
    """Event: raised whenever a deploy is finalized.
    
    :param network_id: Identifier of network upon which a block has been finalized.
    :param bhash: Hash of finalized block.
    :param dhash: Hash of finalized deploy.

    """
    print(f"TODO on_deploy_finalized : {network_id.name} : {bhash} : {dhash}")
