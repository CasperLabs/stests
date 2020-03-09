import enum


class WorkflowDimension(enum.Flag):
    """Flag over set of workflow dimension.
    
    """
    RUN = enum.auto()
    PHASE = enum.auto()
    STEP = enum.auto()


class ExecutionStatus(enum.Flag):
    """Flag over set of execution states.
    
    """
    NULL = enum.auto()
    IN_PROGRESS = enum.auto()
    COMPLETE = enum.auto()
    ERROR = enum.auto()
    

# Full set of enums.
ENUM_SET = {
    ExecutionStatus,
}
