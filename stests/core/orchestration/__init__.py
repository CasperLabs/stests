from stests.core.orchestration.enums import *
from stests.core.orchestration.identifiers import *
from stests.core.orchestration.context import *
from stests.core.orchestration.info import *
from stests.core.orchestration.locks import *
from stests.core.orchestration.state_history import *



# Set of supported classes.
DCLASS_SET = {
    PhaseLock,
    PhaseState,
    ExecutionContext,
    RunIdentifier,
    ExecutionInfo,
    RunLock,
    RunState,
    StepLock,
    StepState,
}

# Full domain type set.
TYPE_SET = DCLASS_SET | ENUM_SET
