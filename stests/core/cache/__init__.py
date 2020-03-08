from stests.core.domain import NetworkIdentifier
from stests.core.domain import RunContext

from stests.core.cache.ops_control import *
from stests.core.cache.ops_infra import *
from stests.core.cache.ops_monitoring import *
from stests.core.cache.ops_state import *

import stests.core.cache.ops_control as control
import stests.core.cache.ops_infra as infra
import stests.core.cache.ops_monitoring as monitoring
import stests.core.cache.ops_state as state



def flush_by_network(network_id: NetworkIdentifier):
    """Flushes all information pertaining to a network.

    :param network_id: A network identifier.

    """
    for partition in (control, infra, monitoring, state):
        partition.flush_by_network(network_id)


def flush_by_run(ctx: RunContext):
    """Flushes all information pertaining to a run.

    :param ctx: Generator run contextual information.

    """
    for partition in (control, state):
        partition.flush_by_run(ctx)
