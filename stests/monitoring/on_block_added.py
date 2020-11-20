import dramatiq

from stests.core.types.infra import Node
from stests.core.types.infra import NodeEventInfo



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.block.added"


@dramatiq.actor(queue_name=_QUEUE)
def callback(node: Node, event_info: NodeEventInfo):   
    """Event: raised whenever a block is added.

    :param node_id: Identifier of node from which event was streamed.
    :param event_info: Node event information.

    """
    print(_QUEUE)
