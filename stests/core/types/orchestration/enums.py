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
    

class ExecutionEventType(enum.Enum):
    """Flag over set of typical execution events.
    
    """
    RUN_END = enum.auto()
    RUN_ERROR = enum.auto()
    RUN_START = enum.auto()
    RUN_START_ABORT = enum.auto()
    
    PHASE_END = enum.auto()
    PHASE_ERROR = enum.auto()
    PHASE_START = enum.auto()
    PHASE_START_ABORT = enum.auto()
    
    STEP_END = enum.auto()
    STEP_ERROR = enum.auto()
    STEP_START = enum.auto()
    STEP_START_ABORT = enum.auto()
    STEP_VERIFICATION_FAILURE = enum.auto()

    WORKFLOW_INVALID = enum.auto()


# Full set of enums.
ENUM_SET = {
    ExecutionAspect,
    ExecutionEventType,
    ExecutionMode,
    ExecutionStatus,
}
