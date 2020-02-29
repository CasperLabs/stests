import redis

from stests.core.cache.stores.partitions import StorePartition
from stests.core.utils import env



# Environment variables required by this module.
class EnvVars:
    # Redis host.
    DB = env.get_var('CACHE_REDIS_DB', 1, int)

    # Redis host.
    HOST = env.get_var('CACHE_REDIS_HOST', "localhost")

    # Redis port.
    PORT = env.get_var('CACHE_REDIS_PORT', 6379, int)


def get_store(partition_type: StorePartition) -> redis.Redis:
    """Returns instance of a redis cache store accessor.

    :returns: An instance of a redis cache store accessor.

    """
    # TODO: 1. cluster connections
    return redis.Redis(
        db=EnvVars.DB,
        host=EnvVars.HOST,
        port=EnvVars.PORT
        )

