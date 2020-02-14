import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.cache import NetworkIdentifier



# Queue to which messages will be dispatched.
_QUEUE = f"monitoring.chain"


@dramatiq.actor(queue_name=f"{_QUEUE}.block")
def do_monitor_blocks(network_id: NetworkIdentifier):   
    """Wires upto chain event streaming.
    
    """
    # Set node.
    node = cache.get_node_at_random(network_id)
    print(node)

    # Wire upto event streams.
    clx.stream_events(node, _on_block_added, _on_block_finalized)

    # Chain.
    return ctx


def _on_block_added(bhash):
    print(f"666 block added {bhash}")


def _on_block_finalized(bhash):
    print(f"777 block finalized {bhash}")
