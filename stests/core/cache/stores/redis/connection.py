import typing
import redis

from stests.core.utils import env



def _get_env_var(
    name: str,
    default: typing.Any = None,
    convertor: typing.Callable = None
    ) -> str:
    """Returns an environment variable's current value.

    """
    name = f'CACHE_REDIS_{name}'
    
    return env.get_var(name, default, convertor)


# Config: redis host.
HOST = _get_env_var('HOST', "localhost")

# Config: redis port.
PORT = _get_env_var('PORT', 6379, int)

# Config: redis database.
DB = _get_env_var('DB', 1, int)


def get_connection(db: int = DB) -> redis.Redis:
    """Returns redis connection.
    
    """
    # TODO: map network id to a redis db.
    # TODO: cluster connections
    return redis.Redis(db=db, host=HOST, port=PORT)
