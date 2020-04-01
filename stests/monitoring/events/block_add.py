import dramatiq

from stests.core.domain import NodeIdentifier
from stests.core.utils import logger



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events"


@dramatiq.actor(queue_name=_QUEUE)
def on_block_added(node_id: NodeIdentifier, block_hash: str):   
    """Event: raised whenever a block is added.

    :param node_id: Identifier of node from which event was streamed.
    :param block_hash: Hash of added block.

    """
    logger.log(f"MTRNG :: {node_id.label} -> block added :: {block_hash}")
