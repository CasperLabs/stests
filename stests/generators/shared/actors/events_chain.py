import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.domain import RunContext



# Queue to which messages will be dispatched.
_QUEUE = f"global.events"


@dramatiq.actor(queue_name=f"{_QUEUE}.chain")
def do_stream_chain_events(ctx: RunContext):   
    """Wires upto chain event streaming.
    
    """
    # Set node.
    # TODO: randomize if node index = 0.
    raise NotImplementedError()
    node = cache.get_ctx_node(ctx)

    # Wire upto event streams.
    clx.stream_events(node, on_block_added=_on_block_added, on_block_finalized=_on_block_finalized)

    # Chain.
    return ctx


def _on_block_added(bhash):
    print(f"666 block added {bhash}")


def _on_block_finalized(bhash):
    print(f"777 block finalized {bhash}")
