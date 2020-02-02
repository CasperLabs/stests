import redis
from dramatiq.rate_limits.backends import RedisBackend
from dramatiq.middleware import GroupCallbacks

from stests.core.utils import env



# Environment variables required by this module.
class EnvVars:
    # Redis host.
    DB = env.get_var('BROKER_REDIS_DB', 0, int)

    # Redis protocol.
    HOST = env.get_var('BROKER_REDIS_HOST', "localhost")

    # Redis port.
    PORT = env.get_var('BROKER_REDIS_PORT', 6379, int)



def get_mware():
    return GroupCallbacks(
        RedisBackend(client=redis.Redis(db=EnvVars.DB, host=EnvVars.HOST, port=EnvVars.PORT))
    )
