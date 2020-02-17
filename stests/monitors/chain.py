import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.cache import NetworkIdentifier
from stests.core.utils import logger

from stests.actors.block import do_process_added_block
from stests.actors.block import do_process_finalized_block


# Queue to which messages will be dispatched.
_QUEUE = "monitors"


@dramatiq.actor(queue_name=_QUEUE)
def do_monitor_blocks(network_id: NetworkIdentifier):   
    """Wires upto chain event streaming.
    
    """
    # Set node.
    node = cache.get_node_by_network_id(network_id)
    
    # Wire upto event streams.
    clx.stream_events(
        node, 
        lambda bhash: do_process_added_block.send(network_id, bhash),
        lambda bhash: do_process_finalized_block.send(network_id, bhash)
        )
