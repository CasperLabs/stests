import dataclasses
import typing

from stests.core.logging.factory import get_monitoring_event_info
from stests.core.logging.factory import get_workflow_event_info
from stests.core.types.infra import NodeEventType
from stests.core.types.orchestration import ExecutionEventType



# Map: event type enum -> event info factory.
_FACTORIES = {
    NodeEventType: get_monitoring_event_info,
    ExecutionEventType: get_workflow_event_info,
}


def log_event(event_type: typing.Union[NodeEventType, ExecutionEventType], *args, **kwargs):
    """Appends event information to event log.

    :param event_type: Type of event being logged.

    """
    info_factory = _FACTORIES[type(event_type)]
    info = info_factory(event_type, *args, **kwargs)
    # TODO - use structlog | logstash ?
    print(f"{info.context.timestamp}Z {info.context.level} {info.context.priority} {info.context.host_name} {info.context.process_id} {info.context.system}:{info.context.sub_system}.{info.context.event_type} payload={dataclasses.asdict(info)}")
