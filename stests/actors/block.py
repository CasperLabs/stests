import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.cache import NetworkIdentifier



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.chain.block"


@dramatiq.actor(queue_name=_QUEUE)
def do_process_added_block(network_id: NetworkIdentifier, bhash: str):   
    """Processes an added block.
    
    """
    # TODO: pull deploys, sync cache & notify downstream.
    print(f"block added :: {network_id} ::: {bhash}")

    # clx.get_block_info(bhash)


@dramatiq.actor(queue_name=_QUEUE)
def do_process_finalized_block(network_id: NetworkIdentifier, bhash: str):   
    """Processes a finalized block.
    
    """
    # TODO: pull deploys, sync cache & notify downstream.
    print(f"block finalized :: {network_id} ::: {bhash}")

    print(clx.get_block_info(network_id, bhash))
