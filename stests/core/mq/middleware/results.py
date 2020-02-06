import redis
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend

from stests.core.utils import env



# Environment variables required by this module.
class EnvVars:
    # Redis host.
    DB = env.get_var('MWARE_REDIS_DB', 0, int)

    # Redis protocol.
    HOST = env.get_var('MWARE_REDIS_HOST', "localhost")

    # Redis port.
    PORT = env.get_var('MWARE_REDIS_PORT', 6379, int)


def get_mware():
    """Returns a broker middleware designed to support making available actor execution results to downstream actors.
    
    """
    return Results(
        RedisBackend(client=redis.Redis(db=EnvVars.DB, host=EnvVars.HOST, port=EnvVars.PORT))
        )
