import json
import typing

from stests.core.cache import stores
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
        return _decode_item(obj)


def do_get_all(store: typing.Callable, search_key: str) -> typing.Any:
    """Wraps redis.mget command.
    
    :param store: Cache store connection wrapper.
    :param search_key: Key woth which to search cache.

    """
    logger.log(f"CACHE :: get :: {search_key}")
    CHUNK_SIZE = 5000
    _, keys = store.scan(match=search_key, count=CHUNK_SIZE)

    return [_decode_item(i) for i in store.mget(keys)] if keys else []


def do_set(store: typing.Callable, key: str, data: typing.Any):
    """Wraps redis.set command.
    
    :param store: Cache store connection wrapper.
    :param key: Key of item to be cached.
    :param data: Data to be cached.

    """
    print(555)
    logger.log(f"CACHE :: set :: key={key}")
    store.set(key, json.dumps(encoder.encode(data), indent=4))

    return key


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
    ns_keys = namespace + ':*'
    while cursor != 0:
        cursor, keys = store.scan(cursor=cursor, match=ns_keys, count=CHUNK_SIZE)
        print(ns_keys, keys)
        if keys:
            store.delete(*keys)

    print(666)

    return True


def _decode_item(obj):
    """Returns a decoded encached domain object.
    
    """
    return encoder.decode(json.loads(obj))


def encache(func):
    """Decorator to orthoganally encache domain objects.
    
    """
    def wrapper(*args, **kwargs):
        key, data = func(*args, **kwargs)
        with stores.get_store() as store:
            do_set(store, key, data)

    return wrapper


def decache(func):
    """Decorator to orthoganally pull domain objects from cache.
    
    """
    def wrapper(*args, **kwargs):
        key = func(*args, **kwargs)
        with stores.get_store() as store:
            if key.endswith("*"):
                return do_get_all(store, key)
            else:
                return do_get(store, key)

    return wrapper