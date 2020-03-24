from stests.core.orchestration.enums import *
from stests.core.orchestration.identifiers import *
from stests.core.orchestration.context import *
from stests.core.orchestration.info import *
from stests.core.orchestration.lock import *
from stests.core.orchestration.state_history import *



# Set of supported classes.
DCLASS_SET = {
    ExecutionContext,
    ExecutionInfo,
    ExecutionLock,
    ExecutionState,
    RunIdentifier,
}

# Full domain type set.
TYPE_SET = DCLASS_SET | ENUM_SET
