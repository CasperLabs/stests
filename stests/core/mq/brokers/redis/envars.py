import typing

from stests.core.utils import env



def _get_env_var(
    name: str,
    default: typing.Any = None,
    convertor: typing.Callable = None
    ) -> str:
    """Returns an environment variable's current value.

    """
    # Apply prefix.
    name = f'MQ_BROKER_REDIS_{name}'

    return env.get_var(name, default, convertor)


# Config: redis db.
DB = _get_env_var('DB', 0, int)

# Config: redis host.
HOST = _get_env_var('HOST', "localhost")

# Config: redis port.
PORT = _get_env_var('PORT', 6379, int)

