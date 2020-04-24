from datetime import datetime

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core import factory
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeIdentifier
from stests.core.utils import logger


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

    # Assert query returned block info - if not then this is an error scenario.
    if block_info is None:
        logger.log_error(f"MONIT :: {node_id.label} -> finalized block query failure :: {block_hash}")
