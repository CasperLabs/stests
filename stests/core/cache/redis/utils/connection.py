import redis

from stests.utils.env import get_env_var



# Default redis host.
DEFAULT_HOST = "localhost"

# Default redis port.
DEFAULT_PORT = 6379


def get_connection() -> redis.Connection:
    """Returns redis connection.
    
    """
    # TODO: cluster connections
    return redis.Redis(host=_HOST, port=_PORT)


def _get_env_var(name, default=None):
    """Returns an environment variable's current value.

    """
    # Apply prefix.
    name = f'CACHE_REDIS_{name}'

    return get_env_var(name, default)


# Cache config: host.
_HOST = _get_env_var('HOST', DEFAULT_HOST)

# Cache config: port.
_PORT = _get_env_var('PORT', DEFAULT_PORT)
