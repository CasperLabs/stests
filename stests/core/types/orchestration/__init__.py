from stests.core.types.orchestration.enums import ExecutionAspect
from stests.core.types.orchestration.enums import ExecutionMode
from stests.core.types.orchestration.enums import ExecutionStatus
from stests.core.types.orchestration.enums import ENUM_SET
from stests.core.types.orchestration.identifier import ExecutionIdentifier
from stests.core.types.orchestration.context import ExecutionContext
from stests.core.types.orchestration.info import ExecutionInfo
from stests.core.types.orchestration.lock import ExecutionLock



TYPE_SET = {
    ExecutionContext,
    ExecutionIdentifier,
    ExecutionInfo,
    ExecutionLock,
} | ENUM_SET
