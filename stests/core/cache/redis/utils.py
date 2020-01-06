import os
import typing

import redis

from stests.core.types.core import ExecutionContext
from stests.utils.env import get_env_var



def get_connection() -> redis.Connection:
    """Returns redis connection.
    
    """
    # TODO: cluster connections
    return redis.Redis(host=_HOST, port=_PORT)


def get_key(ctx: ExecutionContext, item_type: str, item_key: str) -> str:
    """Returns fully qualified cache key.
    
    :param ctx: Contextual information passed along the flow of execution.
    :param item_type: Type of item being cached.
    :param item_key: Key of item to be cached.

    :returns: A fully qualified cache key.

    """
    namespace = _get_namespace(ctx, item_type)

    return f"{namespace}:{item_key}"


def do_set(key: str, data: typing.Any):
    """Execute redis.set command.
    
    :param key: Key of item to be cached.
    :param data: Data to be cached.

    """
    # Auto map domain types to JSON if applicable.
    try:
        data.to_json
    except AttributeError:
        pass
    else:
        data = data.to_json()
    
    # TODO: change connection to context manager
    r = get_connection()
    r.set(key, data)


def _get_namespace(ctx: ExecutionContext, item_type: str = None) -> str:
    """Returns namespace to be prefixed to a key.

    :param ctx: Contextual information passed along the flow of execution.
    :param item_type: Type of item being cached.

    :returns: Namespace to be prefixed to an item key.

    """
    ns = f"{ctx.network_id}.{ctx.generator_id}.{ctx.generator_run}"
    if item_type is not None:
        ns = f"{ns}.{item_type}"

    return ns
    

def _get_env_var(name, default=None):
    """Returns an environment variable's current value.

    """
    # Apply prefix.
    name = f'CACHE_REDIS_{name}'

    return get_env_var(name, default)


# Cache config: host.
_HOST = _get_env_var('HOST', "localhost")

# Cache config: port.
_PORT = _get_env_var('PORT', 6379)