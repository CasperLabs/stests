import dataclasses
import typing

from stests.core.logging.enums import CoreEventType
from stests.core.logging.enums import MonitoringEventType
from stests.core.logging.enums import WorkflowEventType
from stests.core.logging.factory import get_core_event_info
from stests.core.logging.factory import get_monitoring_event_info
from stests.core.logging.factory import get_workflow_event_info



# Map: event type enum -> event info factory.
_FACTORIES = {
    CoreEventType: get_core_event_info,
    MonitoringEventType: get_monitoring_event_info,
    WorkflowEventType: get_workflow_event_info,
}


def log_event(event_type: typing.Union[CoreEventType, MonitoringEventType, WorkflowEventType], *args, **kwargs):
    """Appends event information to event log.

    :param event_type: Type of event being logged.

    """
    from stests.core.utils import encoder

    info_factory = _FACTORIES[type(event_type)]
    info = info_factory(event_type, *args, **kwargs)
    # TODO - use structlog | logstash ?
    print(f"{info.event.timestamp}Z {info.event.level} {info.event.priority} {info.process.host} {info.process.pid} {info.app.system} {info.app.sub_system}.{info.event.type}   payload={encoder.encode(info, False)}")
