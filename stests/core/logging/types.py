import dataclasses
import datetime
import enum
import typing



class Level(enum.Enum):
    """Flag over set of log levels.
    
    """
    DEBUG = enum.auto()
    INFO = enum.auto()
    WARN = enum.auto()
    ERROR = enum.auto()
    CRITICAL = enum.auto()
    FATAL = enum.auto()


class SubSystem(enum.Enum):
    """Flag over set of sub-systems to be logged.
    
    """
    MONITORING = enum.auto()
    WORKFLOW = enum.auto()


@dataclasses.dataclass
class ContextualLogInfo():
    """Contextual log information.
    
    """
    # Event id for disambiguation purpose.
    event_id: str

    # Event type for disambiguation purpose.
    event_type: str

    # Unique identifier.
    event_uid: str

    # Machine upon which system is running.
    host_name: str

    # Event level.
    level: Level

    # Network of which machine is a member.
    net_name: str

    # OS user running system.
    os_user: str

    # Event priority.
    priority: int

    # Process ID.
    process_id: str

    # System emitting event, i.e. STESTS.
    system: str

    # Sub-system emitting event, e.g. CHAIN
    sub_system: str

    # ISO UTC Timestamp.
    timestamp: datetime.datetime


@dataclasses.dataclass
class MonitoringLogInfo:
    """Monitoring event log information.
    
    """
    # Event message.
    message: typing.Optional[str]

    # Associated network.
    network: str

    # Node in respect of which the event was emitted.
    node_index: int

    # Hash of a block.
    block_hash: typing.Optional[str]

    # Hash of a deploy.
    deploy_hash: typing.Optional[str]

    # Contextual meta info.
    context: ContextualLogInfo


@dataclasses.dataclass
class WorkflowLogInfo:
    """Workflow event log information.
    
    """
    # Event message.
    message: typing.Optional[str]

    # Associated network.
    network: str

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str    

    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: int

    # Numerical index to distinguish between multiple phase within a generator.
    phase_index: typing.Optional[int]

    # Numerical index to distinguish between multiple steps within a generator.
    step_index: typing.Optional[int]

    # Label to disambiguate a step within the context of a phase.
    step_label: typing.Optional[str]

    # Contextual meta info.
    context: ContextualLogInfo


# Full type set.
TYPE_SET = {
    Level,
    SubSystem,
    ContextualLogInfo,
    MonitoringLogInfo,
    WorkflowLogInfo,
}
