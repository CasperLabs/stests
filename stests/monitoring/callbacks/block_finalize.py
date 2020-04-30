from datetime import datetime

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core import factory
from stests.core.logging import log_event
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeIdentifier
from stests.events import EventType



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.block.finalized"


@dramatiq.actor(queue_name=_QUEUE)
def on_block_finalized(node_id: NodeIdentifier, event_info: NodeEventInfo):   
    """Event: raised whenever a block is finalized.

    :param node_id: Identifier of node from which event was streamed.
    :param event_info: Node event information.

    """
    block_hash = event_info.block_hash

    # Query: on-chain block info.
    block_info = clx.get_block_info(node_id, block_hash, parse=False)
    if block_info is None:
        log_event(EventType.MONITORING_BLOCK_NOT_FOUND, None, node_id, block_hash=block_hash)
