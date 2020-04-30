import enum



class ExecutionAspect(enum.Enum):
    """Flag over set of aspects of execution.
    
    """
    RUN = enum.auto()
    PHASE = enum.auto()
    STEP = enum.auto()


class ExecutionMode(enum.Enum):
    """Flag over set of execution modes.
    
    """
    SEQUENTIAL = enum.auto()
    PERIODIC = enum.auto()


class ExecutionStatus(enum.Flag):
    """Flag over set of execution states.
    
    """
    NULL = enum.auto()
    IN_PROGRESS = enum.auto()
    COMPLETE = enum.auto()
    ERROR = enum.auto()



# Full set of enums.
ENUM_SET = {
    ExecutionAspect,
    ExecutionMode,
    ExecutionStatus,
}
