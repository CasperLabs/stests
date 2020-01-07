import redis

from stests.utils.env import get_env_var



# Default redis host.
DEFAULT_HOST = "localhost"

# Default redis port.
DEFAULT_PORT = 6379

# Default redis db (there are 16 per cluster).
DEFAULT_DB = 0


def get_connection() -> redis.Connection:
    """Returns redis connection.
    
    """
    db = _get_env_var('DB', DEFAULT_DB)
    host = _get_env_var('HOST', DEFAULT_HOST)
    port = _get_env_var('PORT', DEFAULT_PORT)

    # TODO: cluster connections
    return redis.Redis(db=db, host=host, port=port)


def _get_env_var(name, default=None):
    """Returns an environment variable's current value.

    """
    # Apply prefix.
    name = f'MQ_BROKER_REDIS_{name}'

    return get_env_var(name, default)
