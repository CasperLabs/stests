import typing

import fakeredis

from stests.core.cache.redis.utils.connection import get_connection



def do_set(
    key: str,
    data: typing.Any,
    connection: fakeredis.FakeStrictRedis = None
    ):
    """Executes redis.set command.
    
    :param key: Key of item to be cached.
    :param data: Data to be cached.
    :param connection: Pointer to a module implementing the Redis protocol.

    """
    # Auto map domain types to JSON (if applicable).
    try:
        data.to_json
    except AttributeError:
        pass
    else:
        data = data.to_json()
    
    # Connect & set.
    # TODO: change connection to context manager ?
    r = connection or get_connection()
    r.set(key, data)
