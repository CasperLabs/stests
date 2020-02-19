import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.domain import NetworkIdentifier
from stests.core.utils import logger



# Queue to which messages will be dispatched.
_QUEUE = "monitoring"


@dramatiq.actor(queue_name=_QUEUE)
def do_monitor_blocks(network_id: NetworkIdentifier):   
    """Wires upto chain event streaming.
    
    """
    from stests.core.actors.block import on_block_finalized

    # Set node.
    node = cache.get_node_by_network_id(network_id)
    
    # Wire upto event streams.
    clx.stream_events(node, on_block_finalized=lambda block_hash: on_block_finalized.send(network_id, node.index, block_hash))
