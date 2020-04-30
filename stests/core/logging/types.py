import dataclasses
import datetime
import enum
import typing


class OutputMode(enum.Enum):
    """Flag over set of execution container.
    
    """
    DAEMON = enum.auto()
    INTERACTIVE = enum.auto()


class Level(enum.Enum):
    """Flag over set of log levels.
    
    """
    DEBUG = 1
    INFO = 5
    WARN = 7
    ERROR = 9
    CRITICAL = 99
    FATAL = 999


@dataclasses.dataclass
class ApplicationInfo():
    """Encapsulates information pertaining to the application.
    
    """
    # Company information, i.e. clabs.
    company: str

    # System emitting event, i.e. STESTS.
    system: str

    # Sub-system emitting event, e.g. CORE.
    sub_system: str

    # System version.
    version: str


@dataclasses.dataclass
class EventInfo():
    """Encapsulates information pertaining to the application.
    
    """
    # Event id for disambiguation purpose.
    id: str

    # Event level.
    level: Level

    # Event priority.
    priority: int

    # ISO UTC Timestamp.
    timestamp: datetime.datetime

    # Event type for disambiguation purpose.
    type: str

    # Unique identifier.
    uid: str


@dataclasses.dataclass
class ProcessInfo():
    """Encapsulates information pertaining to the running process.
    
    """
    # Machine upon which system is running.
    host: str

    # Network of which machine is a member.
    net: str

    # OS user running system.
    os_user: str

    # Process ID.
    pid: str


@dataclasses.dataclass
class LogMessage:
    """Simple event log information for basic scenario.
    
    """
    # Application information.
    app: ApplicationInfo

    # Event information.
    event: EventInfo

    # Process information.
    process: ProcessInfo
    
    # Plain text message.
    message: typing.Optional[str]

    # Message data.
    data: typing.Dict[str, typing.Any]


# Full type set.
TYPE_SET = {
    ApplicationInfo,
    EventInfo,
    Level,
    LogMessage,
    ProcessInfo,
}
