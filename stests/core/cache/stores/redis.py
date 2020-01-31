import redis

from stests.core.utils import env



# Environment variables required by this module.
class EnvVars:
    # Redis host.
    HOST = env.get_var('CACHE_REDIS_HOST', "localhost")

    # Redis port.
    PORT = env.get_var('CACHE_REDIS_PORT', 6379, int)


def get_store(network_id: str) -> redis.Redis:
    """Returns instance of a redis cache store accessor.

    :param network_id: Identifier of network being tested, e.g. DEV-LOC-01
    :returns: An instance of a redis cache store accessor.

    """
    # TODO: 1. map network id to a redis db so as to partition when
    #          running tests across multiple networks.
    db = 1
    # TODO: 2. cluster connections

    return redis.Redis(db=db, host=EnvVars.HOST, port=EnvVars.PORT)
