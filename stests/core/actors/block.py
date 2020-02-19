import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.utils import factory
from stests.core.domain import BlockStatus
from stests.core.domain import DeployStatus
from stests.core.domain import NetworkIdentifier



# Queue to which messages will be dispatched.
_QUEUE = "monitoring"


@dramatiq.actor(queue_name=_QUEUE)
def on_block_finalized(network_id: NetworkIdentifier, node: int, block_hash: str):   
    """Event: raised whenever a block is finalized.

    :param network_id: Identifier of network upon which a block has been finalized.
    :param node: Identifier of node reporting a finalized block.
    :param block_hash: Hash of finalized block.

    """
    # Get block info.
    block = clx.get_block(network_id, block_hash)

    # Set block status.
    block.status = BlockStatus.FINALIZED

    # Encache.
    cache.set_network_block(network_id, block)  

    # Enqueue deploys.
    for deploy_hash in clx.get_block_deploys(network_id, block_hash):
        on_deploy_finalized.send(network_id, node, block_hash, block.rank, deploy_hash)


@dramatiq.actor(queue_name=_QUEUE)
def on_deploy_finalized(network_id: NetworkIdentifier, node: int, block_hash: str, block_rank: int, deploy_hash: str):   
    """Event: raised whenever a deploy is finalized.
    
    :param network_id: Identifier of network upon which a block has been finalized.
    :param node: Identifier of node reporting a finalized block.
    :param rank: Rank of finalized block.
    :param block_hash: Hash of finalized block.
    :param deploy_hash: Hash of finalized deploy.

    """
    # Set deploy info.
    deploy = factory.create_deploy(network_id, node, block_hash, block_rank, deploy_hash, DeployStatus.FINALIZED)    

    # Encache.
    cache.set_network_deploy(network_id, deploy)  
