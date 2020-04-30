import enum

from stests.core import CoreEventType
from stests.monitoring import MonitoringEventType
from stests.workflows import WorkflowEventType



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
    CORE = enum.auto()
    MONITORING = enum.auto()
    WORKFLOW = enum.auto()


# Full set of enums.
ENUM_SET = {
    Level,
    SubSystem,
    CoreEventType,
    MonitoringEventType,
    WorkflowEventType,
}
