import dramatiq

from stests import chain
from stests.core import cache
from stests.core import factory
from stests.core.logging import log_event
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeIdentifier
from stests.events import EventType



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.deploy.processed"


@dramatiq.actor(queue_name=_QUEUE)
def on_deploy_processed(info: NodeEventInfo):   
    """Event: raised whenever a deploy is processed.

    :param info: Node event information.

    """
    return
