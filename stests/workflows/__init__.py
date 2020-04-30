import enum



class WorkflowEventType(enum.Enum):
    """Enum over set of sub-system events.
    
    """
    RUN_ABORT = enum.auto()
    RUN_END = enum.auto()
    RUN_ERROR = enum.auto()
    RUN_START = enum.auto()
    
    PHASE_ABORT = enum.auto()
    PHASE_END = enum.auto()
    PHASE_ERROR = enum.auto()
    PHASE_START = enum.auto()
    
    STEP_ABORT = enum.auto()
    STEP_END = enum.auto()
    STEP_ERROR = enum.auto()
    STEP_FAILURE = enum.auto()
    STEP_START = enum.auto()

    WORKFLOW_INVALID = enum.auto()
