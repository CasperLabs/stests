import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.cache import NetworkIdentifier

from stests.monitoring.chain.actors.blocks import do_process_finalized_block


# Queue to which messages will be dispatched.
_QUEUE = "monitoring.chain.block"


@dramatiq.actor(queue_name=_QUEUE)
def do_monitor_blocks(network_id: NetworkIdentifier):   
    """Wires upto chain event streaming.
    
    """
    # Set node.
    node = cache.get_node_at_random(network_id)
    
    # Wire upto event streams.
    clx.stream_events(node, _on_block_added, _on_block_finalized)

    # Chain.
    return ctx


def _on_block_added(bhash): 
    """Callback: block added events.
    
    """
    # TODO: review if this is a useful event or not.
    print(f"block added {bhash}")


def _on_block_finalized(bhash):
    """Callback: block finalized events.
    
    """
    # Dispatch message to downstream worker.
    do_process_finalized_block.send(bhash)
