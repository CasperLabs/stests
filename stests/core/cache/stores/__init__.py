from stests.core.cache.model import StorePartition
from stests.core.cache.stores import redis
from stests.core.cache.stores import stub
from stests.core.utils import env
from stests.core.utils.exceptions import InvalidEnvironmentVariable



# Environment variables required by this module.
class EnvVars:
    # Cache type.
    TYPE = env.get_var("CACHE_TYPE", "REDIS")


# Map: Cache store type -> factory.
FACTORIES = {
    "REDIS": redis,
    "STUB": stub
}


def get_store(partition_type: StorePartition = StorePartition.INFRA):
    """Returns a cache store ready to be used as a state persistence & flow control mechanism.

    :param partition_type: Type of partition to be instantiated.
    :returns: A cache store.

    """ 
    try:
        factory = FACTORIES[EnvVars.TYPE]
    except KeyError:
        raise InvalidEnvironmentVariable("CACHE_TYPE", EnvVars.TYPE, FACTORIES)

    return factory.get_store(partition_type)
