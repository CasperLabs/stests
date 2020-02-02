import redis
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend

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
    backend = RedisBackend(client=redis.Redis(db=EnvVars.DB, host=EnvVars.HOST, port=EnvVars.PORT))

    return Results(backend=backend)
