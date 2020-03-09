from stests.core.orchestration.enums import *
from stests.core.orchestration.locks import *
from stests.core.orchestration.state_history import *

from stests.core.orchestration.phase import *
from stests.core.orchestration.run import *
from stests.core.orchestration.step import *



# Set of supported classes.
DCLASS_SET = {
    ExecutionPhaseInfo,
    ExecutionPhaseLock,
    ExecutionPhaseState,
    ExecutionRunIdentifier,
    ExecutionContextInfo,
    ExecutionRunLock,
    ExecutionRunState,
    ExecutionStepInfo,
    ExecutionStepLock,
    ExecutionStepState,
}

# Full domain type set.
TYPE_SET = DCLASS_SET | ENUM_SET
