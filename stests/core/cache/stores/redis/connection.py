import redis

from stests.core.utils import env



def _get_env_var(name, default=None):
    """Returns an environment variable's current value.

    """
    # Apply prefix.
    name = f'CACHE_REDIS_{name}'

    return env.get_var(name, default)


# Config: redis host.
HOST = _get_env_var('HOST', "localhost")

# Config: redis port.
PORT = _get_env_var('PORT', 6379)

# Config: redis database.
DB = _get_env_var('DB', 1)


def get_connection(db: int = DB) -> redis.Redis:
    """Returns redis connection.
    
    """
    # TODO: map network id to a redis db.
    # TODO: cluster connections
    return redis.Redis(db=db, host=HOST, port=PORT)
