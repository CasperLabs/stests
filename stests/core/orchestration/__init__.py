from stests.core.orchestration.enums import *
from stests.core.orchestration.identifier import *
from stests.core.orchestration.context import *
from stests.core.orchestration.info import *
from stests.core.orchestration.lock import *



# Set of supported classes.
DCLASS_SET = {
    ExecutionContext,
    ExecutionIdentifier,
    ExecutionInfo,
    ExecutionLock,
}

# Full domain type set.
TYPE_SET = DCLASS_SET | ENUM_SET
