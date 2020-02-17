import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.utils import factory
from stests.core.cache import NetworkIdentifier
from stests.core.domain import BlockStatus



# Queue to which messages will be dispatched.
_QUEUE = "monitors.blocks"


@dramatiq.actor(queue_name=_QUEUE)
def on_block_added(network_id: NetworkIdentifier, bhash: str):   
    """Event: raised whenever a new block is added.
    
    """
    # TODO: ???
    print(f"block added :: {network_id} ::: {bhash}")


@dramatiq.actor(queue_name=_QUEUE)
def on_block_finalized(network_id: NetworkIdentifier, bhash: str):   
    """Event: raised whenever a block is finalized.
    
    """
    # TODO: pull deploys, sync cache & notify downstream.
    # Set block info.
    block = clx.get_block(network_id, bhash)

    # Set block status.
    block.status = BlockStatus.FINALIZED

    # Update cache.
    cache.set_block(network_id, block)

    # Enqueue deploys.
    for dhash in (i.deploy.deploy_hash.hex() for i in clx.get_block_deploys(network_id, bhash)):
        do_process_finalized_deploy.send(network_id, bhash, dhash)


@dramatiq.actor(queue_name=_QUEUE)
def do_process_finalized_deploy(network_id: NetworkIdentifier, bhash: str, dhash: str):   
    """Processes a finalized deploy.
    
    """
    print(f"TODO do_process_finalized_deploy : {network_id.name} : {bhash} : {dhash}")
