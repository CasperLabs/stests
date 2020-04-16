from stests.core.types.orchestration.enums import *
from stests.core.types.orchestration.identifier import *
from stests.core.types.orchestration.context import *
from stests.core.types.orchestration.info import *
from stests.core.types.orchestration.lock import *



# Set of supported classes.
DCLASS_SET = {
    ExecutionContext,
    ExecutionIdentifier,
    ExecutionInfo,
    ExecutionLock,
}

# Full domain type set.
TYPE_SET = DCLASS_SET | ENUM_SET
