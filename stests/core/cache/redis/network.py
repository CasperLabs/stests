import redis

from stests.core.cache.redis.utils import get_key
from stests.core.cache.redis.utils import do_set
from stests.core.types.core import ExecutionContext
from stests.core.types.network import Network



def append(network: Network):
    """Appends network information to cache store.

    :param ctx: Contextual information passed along the flow of execution.
    :param network: Network information being cached.

    :returns: Network's cache key.

    """
    # Set key.
    key = network.name

    # Push to cache store.
    do_set(key, network)

    return key
