import dataclasses
import enum
import typing
import uuid
from datetime import datetime



class EventType(enum.Enum):
    """Enum over set of system events.
    
    """
    # Core sub-system.
    CORE_BROKER_CONNECTION_ESTABLISHED = enum.auto()
    CORE_ENCODING_FAILURE = enum.auto()
    CORE_ACTOR_ERROR = enum.auto()    

    # Chain info reporting sub-system.
    CHAININFO_BLOCK = enum.auto()
    CHAININFO_BLOCK_SUMMARY = enum.auto()
    CHAININFO_DEPLOY = enum.auto()
    CHAININFO_DEPLOY_SUMMARY = enum.auto()

    # Monitoring sub-system.
    MONITORING_API_ERROR = enum.auto()
    MONITORING_ACCOUNT_NOT_FOUND = enum.auto()
    MONITORING_BLOCK_ADD = enum.auto()
    MONITORING_BLOCK_FINALIZED = enum.auto()
    MONITORING_BLOCK_FINALIZED_INFO = enum.auto()
    MONITORING_BLOCK_NOT_FOUND = enum.auto()
    MONITORING_DEPLOY_ADDED = enum.auto()
    MONITORING_DEPLOY_CORRELATED = enum.auto()
    MONITORING_DEPLOY_DISCARDED = enum.auto()
    MONITORING_DEPLOY_DISPATCHED = enum.auto()
    MONITORING_DEPLOY_FINALIZED = enum.auto()
    MONITORING_DEPLOY_NOT_FOUND = enum.auto()
    MONITORING_DEPLOY_ORPHANED = enum.auto()
    MONITORING_DEPLOY_PROCESSED = enum.auto()
    MONITORING_DEPLOY_REQUEUED = enum.auto()    
    MONITORING_STREAM_OPENING = enum.auto()
    MONITORING_STREAM_EVENT_TYPE_UNKNOWN = enum.auto()

    # Workflow sub-system.
    WORKFLOW_RUN_ABORT = enum.auto()
    WORKFLOW_RUN_END = enum.auto()
    WORKFLOW_RUN_ERROR = enum.auto()
    WORKFLOW_RUN_START = enum.auto()
    WORKFLOW_PHASE_ABORT = enum.auto()
    WORKFLOW_PHASE_END = enum.auto()
    WORKFLOW_PHASE_ERROR = enum.auto()
    WORKFLOW_PHASE_START = enum.auto()
    WORKFLOW_STEP_ABORT = enum.auto()
    WORKFLOW_STEP_END = enum.auto()
    WORKFLOW_STEP_ERROR = enum.auto()
    WORKFLOW_STEP_FAILURE = enum.auto()
    WORKFLOW_STEP_START = enum.auto()
    WORKFLOW_INVALID = enum.auto()
    WORKFLOW_GENERATOR_LAUNCHED = enum.auto()


# Set of error events.
EVENTS_ERROR = (
    EventType.CORE_ACTOR_ERROR,
    EventType.MONITORING_DEPLOY_DISCARDED,
    EventType.MONITORING_DEPLOY_ORPHANED,
    EventType.MONITORING_API_ERROR,
    EventType.WORKFLOW_RUN_ERROR,
    EventType.WORKFLOW_PHASE_ERROR,
    EventType.WORKFLOW_STEP_ERROR,
)


# Set of warning events.
EVENTS_WARN = (
    EventType.CORE_ENCODING_FAILURE,
    EventType.MONITORING_ACCOUNT_NOT_FOUND,
    EventType.MONITORING_BLOCK_NOT_FOUND,
    EventType.MONITORING_DEPLOY_REQUEUED,
    EventType.MONITORING_STREAM_EVENT_TYPE_UNKNOWN,
    EventType.WORKFLOW_RUN_ABORT,
    EventType.WORKFLOW_PHASE_ABORT,
    EventType.WORKFLOW_STEP_ABORT,
    EventType.WORKFLOW_STEP_FAILURE,
)


@dataclasses.dataclass
class EventInfo():
    """Encapsulates information pertaining to the application.
    
    """
    # Event data.
    data: dict

    # Event id for disambiguation purpose.
    id: str

    # Event message.
    message: str

    # Event name.
    name: str

    # Event priority.
    priority: int

    # ISO UTC Timestamp.
    timestamp: datetime

    # Event type for disambiguation purpose.
    type: EventType

    # Unique identifier.
    uid: str

    @property
    def sub_system(self):
        return self.type.name.split("_")[0]


def get_event_info(event_type: EventType, message: typing.Union[BaseException, str], *args, **kwargs) -> EventInfo:
    """Returns sub-system event information.
    
    """
    event_name = "_".join(event_type.name.split('_')[1:])
    sub_system = event_type.name.split('_')[0]

    if sub_system == "CORE":
        event_id, data = event_type.value, dict()
    elif sub_system == "CHAININFO":
        event_id, data = _get_event_info_chaininfo(event_type, *args, **kwargs)
    elif sub_system == "MONITORING":
        event_id, data = _get_event_info_monitoring(event_type, *args, **kwargs)
    elif sub_system == "WORKFLOW":
        event_id, data = _get_event_info_workflow(event_type, *args, **kwargs)

    return EventInfo(
        data=data,
        id=event_id,
        message=f"{event_name} :: {str(message)}" if message else event_name,
        name=event_name,
        priority=9 if event_type in EVENTS_ERROR else 7 if event_type in EVENTS_WARN else 5,
        timestamp=datetime.utcnow().timestamp(),
        type=event_type,
        uid=str(uuid.uuid4()),
    )


def _get_event_info_chaininfo(
    event_type: EventType,
    node: typing.Any,
    data: typing.Any,
    ) -> typing.Tuple[str, int, dict]:
    """Returns monitoring sub-system event information.
    
    """
    return event_id or event_type.value, data


def _get_event_info_monitoring(
    event_type: EventType,
    node: typing.Any,
    event_id: int = None,
    block_hash: str = None,
    deploy_hash: str = None,
    ) -> typing.Tuple[str, int, dict]:
    """Returns monitoring sub-system event information.
    
    """
    return event_id or event_type.value, {
        'network': node.network_name,
        'node': node.label_index,
        'block': block_hash,
        'deploy': deploy_hash,
    }


def _get_event_info_workflow(event_type: EventType, ctx: typing.Any) -> typing.Tuple[str, int, dict]:
    """Returns workflow sub-system event information.
    
    """
    return event_type.value, {
        'network': ctx.network,
        'phase_index': ctx.phase_index,
        'run_index': ctx.run_index,
        'run_type': ctx.run_type,
        'step_index': ctx.step_index,
        'step_label': ctx.step_label,  
    }
