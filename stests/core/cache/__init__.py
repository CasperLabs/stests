from stests.core.domain import NetworkIdentifier
from stests.core.types.orchestration import ExecutionContext

import stests.core.cache.ops_infra as infra
import stests.core.cache.ops_monitoring as monitoring
import stests.core.cache.ops_orchestration as orchestration
import stests.core.cache.ops_state as state



def flush_by_run(ctx: ExecutionContext):
    """Flushes all information pertaining to a run.

    :param ctx: Execution context information.

    """
    for partition in (orchestration, state):
        partition.flush_by_run(ctx)
