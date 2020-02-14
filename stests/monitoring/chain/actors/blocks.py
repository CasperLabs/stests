import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.cache import NetworkIdentifier



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.chain.block"


@dramatiq.actor(queue_name=_QUEUE)
def do_process_finalized_block(bhash: str):   
    """Processes a finalized block.
    
    """
    # TODO: pull deploys, sync cache & notify downstream.
    print(f"{bhash}")
