import json
import typing

from stests.core.cache.stores import get_store
from stests.core.utils import encoder
from stests.core.utils import logger



def do_delete(store: typing.Callable, key: str):
    """Wraps redis.delete command.
    
    :param store: Cache store connection wrapper.
    :param key: Key of item to be uncached.

    """
    logger.log(f"CACHE :: delete :: {key}")
    store.delete(key)


def do_get(store: typing.Callable, key: str) -> typing.Any:
    """Wraps redis.get command.
    
    :param store: Cache store connection wrapper.
    :param key: Key of item to be cached.

    """
    logger.log(f"CACHE :: get :: {key}")
    obj = store.get(key)
    if obj is None:
        logger.log_warning(f"CACHE :: get :: {key} :: not found")
    else:
        return encoder.decode(json.loads(obj))


def do_set(store: typing.Callable, key: str, data: typing.Any):
    """Wraps redis.set command.
    
    :param store: Cache store connection wrapper.
    :param key: Key of item to be cached.
    :param data: Data to be cached.

    """
    logger.log(f"CACHE :: set :: {key}")
    store.set(key, json.dumps(encoder.encode(data), indent=4))


def get_key(namespace: str, item_key: str) -> str:
    """Returns fully qualified cache key.
    
    :param namespace: Namespace to prefix key with.
    :param item_key: Key of item being cached.

    :returns: A fully qualified cache key.

    """
    return f"{namespace}:{item_key}"


def flush_namespace(store: typing.Callable, namespace: str) -> bool:
    """Clears a namespace.

    :param ns: namespace i.e your:prefix
    :returns: True if cleared.

    """
    CHUNK_SIZE = 5000
    cursor = '0'
    ns_keys = namespace + '*'
    while cursor != 0:
        cursor, keys = store.scan(cursor=cursor, match=ns_keys, count=CHUNK_SIZE)
        if keys:
            store.delete(*keys)

    return True
