import typing

from stests.core.clx.utils import get_client
from stests.core.domain import Node
from stests.core.utils import logger



def execute(
    node: Node,
    on_block_added: typing.Callable = None,
    on_block_finalized: typing.Callable = None
    ):
    """Hooks upto node streaming events.

    :param node: Node from which events will be streamed.
    :param on_block_added: Callback to invoke whenever a block is added to chain.
    :param on_block_finalized: Callback to invoke whenever a block is finalized.

    """
    for event in _yield_events(node, on_block_added, on_block_finalized):
        if on_block_added and event.HasField("block_added"):
            added_block_hash = event.block_added.block.summary.block_hash.hex()
            logger.log(f"Block added :: {added_block_hash}")
            on_block_added(added_block_hash)

        elif on_block_finalized and event.HasField("new_finalized_block"):
            finalized_block_hash = event.new_finalized_block.block_hash
            logger.log(f"Block finalized :: {finalized_block_hash}")
            on_block_finalized(finalized_block_hash)


def _yield_events(node, on_block_added, on_block_finalized):
    """Yields events from event source (i.e. a CLX chain).
    
    """
    # TODO: handle client disconnects.
    client = get_client(node)
    logger.log(f"PYCLX :: stream_events :: connecting to node ...")
    for event in client.stream_events(
        block_added=on_block_added is not None,
        block_finalized=on_block_finalized is not None
        ):
        yield event
