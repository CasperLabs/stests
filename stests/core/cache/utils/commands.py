import typing

from stests.core.utils.execution import ExecutionContext



def do_set(
    ctx: ExecutionContext,
    key: str,
    data: typing.Any
    ):
    """Executes redis.set command.
    
    :param key: Key of item to be cached.
    :param data: Data to be cached.
    :param store: Pointer to a cache store.

    """
    # Auto map domain types to JSON (if applicable).
    try:
        data.to_json
    except AttributeError:
        pass
    else:
        data = data.to_json()
    
    # Write to cache.
    ctx.services.cache.set(key, data)
