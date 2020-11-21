import dramatiq

from stests import chain
from stests.core import cache
from stests.core import factory
from stests.core.logging import log_event
from stests.core.types.chain import BlockStatus
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeIdentifier
from stests.events import EventType



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.block.added"


@dramatiq.actor(queue_name=_QUEUE)
def on_block_added(info: NodeEventInfo):   
    """Event: raised whenever a block is added.

    :param info: Node event information.

    """
    # Escape if already processed.
    if _already_processed(info):
        return

    # Set network / node.
    network_id = factory.create_network_id(info.network)
    network = cache.infra.get_network(network_id)
    node_id = factory.create_node_id(network_id, info.node_index)
    node = cache.infra.get_node(node_id)

    # Set block - escape if not found.
    try:
        block = chain.get_block(network, node, info.block_hash)
    except Exception as err:
        print(f"block query error :: {info.block_hash} :: {err}")
        log_event(EventType.CHAIN_QUERY_BLOCK_NOT_FOUND, None, info.block_hash)
        return

    print(f"monitoring.events.block.added :: {info}")


def _already_processed(info: NodeEventInfo) -> bool:
    """Returns flag indicating whether finalised deploy event has already been processed.

    """
    # Set summary information.
    summary = factory.create_block_summary(info, BlockStatus.ADDED)
    
    # Attempt to cache.
    _, encached = cache.monitoring.set_block_summary(summary)

    # Return flag indicating whether the block has eefectively already been processed.
    return not encached
