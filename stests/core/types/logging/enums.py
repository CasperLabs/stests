import enum



class Level(enum.Enum):
    """Flag over set of log levels.
    
    """
    DEBUG = 1
    INFO = 5
    WARN = 7
    ERROR = 9
    CRITICAL = 99
    FATAL = 999


class OutputMode(enum.Enum):
    """Flag over sets of execution container.
    
    """
    DAEMON = enum.auto()
    INTERACTIVE = enum.auto()


# Full set of enums.
ENUM_SET = {
    Level,    
    OutputMode,
}
