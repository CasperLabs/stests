from stests.core.cache.locks import *
from stests.core.cache.ops_infra import *
from stests.core.cache.ops_monitoring import *
from stests.core.cache.ops_run import *

from stests.core.cache.ops_infra import * as infra
from stests.core.cache.ops_monitoring import * as monitoring
from stests.core.cache.ops_run import * as run



def flush_by_network(network_id: NetworkIdentifier):
    """Flushes all information pertaining to a network.

    :param network_id: A network identifier.

    """
    infra.flush_by_network(network_id)
    monitoring.flush_by_network(network_id)
    run.flush_by_network(network_id)
