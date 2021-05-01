import dataclasses
import enum
import typing
from datetime import datetime


class EventType(enum.Enum):
    """Enum over set of system events.

    """
    # Core sub-system.
    CORE_BROKER_CONNECTION_ESTABLISHED = enum.auto()
    CORE_ENCODING_FAILURE = enum.auto()
    CORE_ACTOR_ERROR = enum.auto()

    # Chain info reporting sub-system.
    CHAIN_ADDED_BLOCK = enum.auto()
    CHAIN_ADDED_BLOCK_EMPTY = enum.auto()
    CHAIN_ADDED_DEPLOY = enum.auto()

    CHAIN_FINALIZED_BLOCK = enum.auto()
    CHAIN_FINALIZED_BLOCK_EMPTY = enum.auto()
    CHAIN_FINALIZED_DEPLOY = enum.auto()

    CHAIN_QUERY_BALANCE = enum.auto()
    CHAIN_QUERY_BALANCE_NOT_FOUND = enum.auto()
    CHAIN_QUERY_BLOCK = enum.auto()
    CHAIN_QUERY_BLOCK_NOT_FOUND = enum.auto()
    CHAIN_QUERY_DEPLOY = enum.auto()
    CHAIN_QUERY_DEPLOY_NOT_FOUND = enum.auto()
    CHAIN_QUERY_STATE = enum.auto()

    # Monitoring sub-system.
    MONIT_BLOCK_ADDED = enum.auto()
    MONIT_BLOCK_FINALIZED = enum.auto()
    MONIT_CONSENSUS_FAULT = enum.auto()
    MONIT_CONSENSUS_FINALITY_SIGNATURE = enum.auto()
    MONIT_DEPLOY_EXECUTION_ERROR = enum.auto()
    MONIT_DEPLOY_PROCESSED = enum.auto()
    MONIT_STEP = enum.auto()
    MONIT_STREAM_BIND_ERROR = enum.auto()
    MONIT_STREAM_EVENT_TYPE_UNKNOWN = enum.auto()
    MONIT_STREAM_OPENING = enum.auto()

    # Workflow sub-system: deploys.
    WFLOW_DEPLOY_CORRELATED = enum.auto()
    WFLOW_DEPLOY_DISPATCHED = enum.auto()
    WFLOW_DEPLOY_DISPATCH_FAILURE = enum.auto()
    WFLOW_DEPLOY_DISPATCH_ERROR = enum.auto()

    # Workflow sub-system: engine.
    WFLOW_RUN_ABORT = enum.auto()
    WFLOW_RUN_END = enum.auto()
    WFLOW_RUN_ERROR = enum.auto()
    WFLOW_RUN_START = enum.auto()
    WFLOW_PHASE_ABORT = enum.auto()
    WFLOW_PHASE_END = enum.auto()
    WFLOW_PHASE_ERROR = enum.auto()
    WFLOW_PHASE_START = enum.auto()
    WFLOW_STEP_ABORT = enum.auto()
    WFLOW_STEP_END = enum.auto()
    WFLOW_STEP_ERROR = enum.auto()
    WFLOW_STEP_FAILURE = enum.auto()
    WFLOW_STEP_START = enum.auto()
    WFLOW_INVALID = enum.auto()
    WFLOW_GENERATOR_LAUNCHED = enum.auto()
    WFLOW_GENERATORS_LAUNCHED = enum.auto()

# Set of debug events.
EVENTS_DEBUG = (
    EventType.CORE_BROKER_CONNECTION_ESTABLISHED,
    EventType.MONIT_BLOCK_ADDED,
    EventType.MONIT_BLOCK_FINALIZED,
    EventType.MONIT_DEPLOY_PROCESSED,
)

# Set of error events.
EVENTS_ERROR = (
    EventType.CORE_ACTOR_ERROR,
    EventType.CHAIN_QUERY_BLOCK_NOT_FOUND,
    EventType.CHAIN_QUERY_DEPLOY_NOT_FOUND,
    EventType.MONIT_DEPLOY_EXECUTION_ERROR,
    EventType.MONIT_STREAM_BIND_ERROR,
    EventType.WFLOW_DEPLOY_DISPATCH_ERROR,
    EventType.WFLOW_RUN_ERROR,
    EventType.WFLOW_PHASE_ERROR,
    EventType.WFLOW_STEP_ERROR,
)


# Set of warning events.
EVENTS_WARN = (
    EventType.CORE_ENCODING_FAILURE,
    EventType.CHAIN_QUERY_BALANCE_NOT_FOUND,
    EventType.WFLOW_DEPLOY_DISPATCH_FAILURE,
    EventType.MONIT_STREAM_EVENT_TYPE_UNKNOWN,
    EventType.WFLOW_RUN_ABORT,
    EventType.WFLOW_PHASE_ABORT,
    EventType.WFLOW_STEP_ABORT,
    EventType.WFLOW_STEP_FAILURE,
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
    elif sub_system == "CHAIN":
        event_id, message, data = _get_event_info_chaininfo(event_type, message, *args, **kwargs)
    elif sub_system == "MONIT":
        event_id, message, data = _get_event_info_monitoring(event_type, message, *args, **kwargs)
    elif sub_system == "WFLOW":
        if event_name.startswith("DEPLOY_"):
            event_id, message, data = _get_event_info_monitoring(event_type, message, *args, **kwargs)
        else:
            event_id, message, data = _get_event_info_workflow(event_type, message, *args, **kwargs)

    return EventInfo(
        data=data,
        id=event_id,
        message=f"{event_type.name} :: {str(message)}" if message else f"{event_type.name}",
        name=event_type.name,
        priority=9 if event_type in EVENTS_ERROR else 7 if event_type in EVENTS_WARN else 1 if event_type in EVENTS_DEBUG else 5,
        timestamp=datetime.utcnow().timestamp(),
        type=event_type,
    )


def _get_event_info_chaininfo(
    event_type: EventType,
    message: typing.Union[str, None],
    info: typing.Any,
    ) -> typing.Tuple[int, dict]:
    """Returns monitoring sub-system event information.

    """
    return event_type.value, message, info


def _get_event_info_monitoring(
    event_type: EventType,
    message: typing.Union[str, None],
    node: typing.Any,
    event_id: int = None,
    block_hash: str = None,
    deploy_hash: str = None,
    ) -> typing.Tuple[int, dict]:
    """Returns monitoring sub-system event information.

    """
    data = {
        'network': node.network_name,
        'node': node.address_rpc if hasattr(node, "address_rpc") else node.label_index,
    }
    if block_hash:
        data['block_hash'] = block_hash
    if deploy_hash:
        data['deploy_hash'] = deploy_hash

    return event_id or event_type.value, message, data


def _get_event_info_workflow(
    event_type: EventType,
    message: typing.Union[str, None],
    ctx: typing.Any,
    ) -> typing.Tuple[int, dict]:
    """Returns workflow sub-system event information.

    """
    return event_type.value, message, {
        'network': ctx.network,
        'phase_index': ctx.phase_index,
        'run_index': ctx.run_index,
        'run_type': ctx.run_type,
        'step_index': ctx.step_index,
        'step_label': ctx.step_label,
    }
