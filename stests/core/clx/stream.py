import typing

from stests.core.clx.utils import get_client
from stests.core.domain import NetworkIdentifier
from stests.core.domain import NodeIdentifier
from stests.core.utils import logger



def stream_events(
    src: typing.Union[NodeIdentifier, NetworkIdentifier],
    on_block_added: typing.Callable = None,
    on_block_finalized: typing.Callable = None
    ):
    """Hooks upto network streaming events.

    :param src: The source from which a network node will be derived.
    :param on_block_added: Callback to invoke whenever a block is added to chain.
    :param on_block_finalized: Callback to invoke whenever a block is finalized.

    """
    for node, event in _yield_events(src, on_block_added, on_block_finalized):
        if on_block_added and event.HasField("block_added"):
            bhash = event.block_added.block.summary.block_hash.hex()
            logger.log(f"PYCLX :: stream_events :: block added :: {bhash}")
            on_block_added(node, bhash)

        elif on_block_finalized and event.HasField("new_finalized_block"):
            bhash = event.new_finalized_block.block_hash.hex()
            logger.log(f"PYCLX :: stream_events :: block finalized :: {bhash}")
            on_block_finalized(node, bhash)


def _yield_events(src: typing.Union[NodeIdentifier, NetworkIdentifier], on_block_added, on_block_finalized):
    """Yields events from event source (i.e. a CLX chain).
    
    """
    # TODO: handle client disconnects.
    logger.log(f"PYCLX :: stream_events :: connecting ...")
    node, client = get_client(src)
    for event in client.stream_events(
        block_added=on_block_added is not None,
        block_finalized=on_block_finalized is not None
        ):
        yield node, event
