import dramatiq

from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeIdentifier



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.deploy.processed"


@dramatiq.actor(queue_name=_QUEUE)
def callback(node_id: NodeIdentifier, event_info: NodeEventInfo):   
    """Event: raised whenever a deploy is processed.

    :param node_id: Identifier of node from which event was streamed.
    :param event_info: Node event information.

    """
    print(_QUEUE)
