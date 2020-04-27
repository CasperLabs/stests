import dataclasses
import datetime
import enum
import typing



class LogLevel(enum.Enum):
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
    CHAIN = enum.auto()
    WFLOW = enum.auto()


@dataclasses.dataclass
class LogInfoMetadata():
    """A log event base class.
    
    """
    # Machine upon which system is running.
    host_name: str

    # Event id for disambiguation purpose.
    event_id: str

    # Event type for disambiguation purpose.
    event_type: str

    # Unique identifier.
    event_uid: str

    # Event level.
    log_level: LogLevel

    # OS user running system.
    os_user: str

    # Event priority.
    priority: int

    # Process ID.
    process_id: str

    # Process ID.
    process_name: str

    # System emitting event, i.e. STESTS.
    system: str

    # Sub-system emitting event, e.g. CHAIN
    sub_system: str

    # Thread ID. d
    thread_id: str

    # ISO UTC Timestamp.
    timestamp: datetime.datetime


@dataclasses.dataclass
class MonnitoringEventLogInfo:
    """Monitoring event log information.
    
    """
    # Associated network.
    network: str

    # Node in respect of which the event was emitted.
    node_index: int

    # Hash of a block.
    block_hash: typing.Optional[str]

    # Hash of a deploy.
    deploy_hash: typing.Optional[str]

    # Event message.
    message: typing.Optional[str]

    # Event metadata.
    meta: LogInfoMetadata


@dataclasses.dataclass
class WorkflowEventLogInfo:
    """Workflow event log information.
    
    """
    # Event message.
    message: typing.Optional[str]

    # Associated network.
    network: str

    # Numerical index to distinguish between multiple phase within a generator.
    phase_index: typing.Optional[int]

    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: int

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str    

    # Numerical index to distinguish between multiple steps within a generator.
    step_index: typing.Optional[int]

    # Label to disambiguate a step within the context of a phase.
    step_label: typing.Optional[str]

    # Event metadata.
    meta: LogInfoMetadata

