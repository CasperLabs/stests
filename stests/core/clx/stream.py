import typing

from stests.core.clx.utils import get_client
from stests.core.domain import NetworkIdentifier
from stests.core.utils import logger



def stream_events(network_id: NetworkIdentifier, on_block_added: typing.Callable = None, on_block_finalized: typing.Callable = None):
    """Hooks upto network streaming events.

    :param network_id: A network identifier.
    :param on_block_added: Callback to invoke whenever a block is added to chain.
    :param on_block_finalized: Callback to invoke whenever a block is finalized.

    """
    for event in _yield_events(network_id, on_block_added, on_block_finalized):
        if on_block_added and event.HasField("block_added"):
            added_block_hash = event.block_added.block.summary.block_hash.hex()
            logger.log(f"PYCLX :: stream_events :: block added :: {added_block_hash}")
            on_block_added(added_block_hash)

        elif on_block_finalized and event.HasField("new_finalized_block"):
            finalized_block_hash = event.new_finalized_block.block_hash.hex()
            logger.log(f"PYCLX :: stream_events :: block finalized :: {finalized_block_hash}")
            on_block_finalized(finalized_block_hash)


def _yield_events(network_id: NetworkIdentifier, on_block_added, on_block_finalized):
    """Yields events from event source (i.e. a CLX chain).
    
    """
    # TODO: handle client disconnects.
    logger.log(f"PYCLX :: stream_events :: connecting ...")
    for event in get_client(network_id).stream_events(
        block_added=on_block_added is not None,
        block_finalized=on_block_finalized is not None
        ):
        yield event
