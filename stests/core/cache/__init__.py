from stests.core.domain import NetworkIdentifier
from stests.core.orchestration import ExecutionRunInfo

import stests.core.cache.ops_infra as infra
import stests.core.cache.ops_monitoring as monitoring
import stests.core.cache.ops_orchestration as orchestration
import stests.core.cache.ops_state as state



def flush_by_network(network_id: NetworkIdentifier):
    """Flushes all information pertaining to a network.

    :param network_id: A network identifier.

    """
    for partition in (infra, monitoring, orchestration, state):
        partition.flush_by_network(network_id)


def flush_by_run(ctx: ExecutionRunInfo):
    """Flushes all information pertaining to a run.

    :param ctx: Generator run contextual information.

    """
    for partition in (orchestration, state):
        partition.flush_by_run(ctx)
