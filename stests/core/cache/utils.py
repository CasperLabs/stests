import json
import typing
import dataclasses
import functools

from stests.core.cache.partitions import StorePartition
from stests.core.cache import stores
from stests.core.utils import encoder
from stests.core.utils import logger



def cache_op(partition: StorePartition):
    """Decorator to orthoganally process a cache operation.

    :param on_success: Continuation function upon execution success.
    :param is_substep: Flag indicating whether decorated function is a sub-step or not.

    :returns: Decorated function.
    
    """
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
                        
            return func(*args, **kwargs)

        return wrapper

    return decorator


def decache(func: typing.Callable) -> typing.Callable:
    """Decorator to orthoganally pull domain objects from cache.

    :param func: Inner function being decorated.

    :returns: Wrapped function.
    
    """
    def wrapper(*args, **kwargs):
        keypath = func(*args, **kwargs)
        key = ":".join([str(i) for i in keypath])
        with stores.get_store() as store:
            if key.find("*") >= 0:
                return _get_all(store, key)
            else:
                return _get(store, key)

    return wrapper


def pull_count(func: typing.Callable) -> typing.Callable:
    """Decorator to orthoganally pull a count from cache.

    :param func: Inner function being decorated.

    :returns: Wrapped function.
    
    """
    def wrapper(*args, **kwargs) -> int:
        keypath = func(*args, **kwargs)
        key = ":".join([str(i) for i in keypath])
        with stores.get_store() as store:
            return int(store.get(key))

    return wrapper


def encache(func: typing.Callable) -> typing.Callable:
    """Decorator to orthoganally push domain objects to cache.
    
    :param func: Inner function being decorated.

    :returns: Wrapped function.

    """
    def wrapper(*args, **kwargs):
        keypath, data = func(*args, **kwargs)
        key = ":".join([str(i) for i in keypath])
        with stores.get_store() as store:
            _set(store, key, data)
        return key

    return wrapper


def encache_lock(func: typing.Callable) -> typing.Callable:
    """Decorator to orthoganally push domain objects to cache (if they have not already been pushed).
    
    :param func: Inner function being decorated.

    :returns: Wrapped function.

    """
    def wrapper(*args, **kwargs):
        keypath, data = func(*args, **kwargs)
        data = dataclasses.asdict(data)
        key = ":".join([str(i) for i in keypath])
        with stores.get_store() as store:
            return key, _setnx(store, key, data)

    return wrapper


def encache_singleton(func: typing.Callable) -> typing.Callable:
    """Decorator to orthoganally push domain objects to cache (if they have not already been pushed).
    
    :param func: Inner function being decorated.

    :returns: Wrapped function.

    """
    def wrapper(*args, **kwargs):
        keypath, data = func(*args, **kwargs)
        key = ":".join([str(i) for i in keypath])
        with stores.get_store() as store:
            was_cached = _setnx(store, key, data)
        return key, was_cached

    return wrapper


def flushcache(func: typing.Callable) -> typing.Callable:
    """Decorator to orthoganally flush domain objects from cache.
    
    :param func: Inner function being decorated.

    :returns: Wrapped function.

    """    
    def wrapper(*args, **kwargs):
        for keypaths in func(*args, **kwargs):
            key = ":".join([str(i) for i in keypaths])
            with stores.get_store() as store:
                _flush(store, key)

    return wrapper


def do_incrby(func: typing.Callable) -> typing.Callable:
    """Decorator to orthoganally push domain objects to cache.
    
    :param func: Inner function being decorated.

    :returns: Wrapped function.

    """
    def wrapper(*args, **kwargs):
        keypath = func(*args, **kwargs)
        key = ":".join([str(i) for i in keypath])
        with stores.get_store() as store:
            store.incrby(key, 1)

    return wrapper


def _decode_item(as_json: str) -> typing.Any:
    """Returns a decoded encached domain object(s).

    :param as_json: JSON representation of cached domain object(s).

    :returns: Domain object(s).

    """
    return encoder.decode(json.loads(as_json))
    

def _delete(store: typing.Callable, key: str):
    """Wraps redis.delete command.
    
    :param store: Cache store connection wrapper.
    :param key: Key of item to be deleted.

    """
    logger.log(f"CACHE :: delete :: {key}")
    store.delete(key)


def _flush(store: typing.Callable, ns_keys: str):
    """Flushes data from cache.

    :param namespace: Namespace to be flushed.

    """
    CHUNK_SIZE = 1000
    cursor = '0'
    while cursor != 0:
        cursor, keys = store.scan(cursor=cursor, match=ns_keys, count=CHUNK_SIZE)
        if keys:
            store.delete(*keys)


def _get(store: typing.Callable, key: str) -> typing.Any:
    """Wraps redis.get command.
    
    :param store: Cache store connection wrapper.
    :param key: Key of item to be retrieved.

    :returns: If a key match then decoded domain object(s), else None.

    """
    logger.log(f"CACHE :: get :: {key}")
    obj = store.get(key)
    if obj is None:
        logger.log_warning(f"CACHE :: get :: {key} :: not found")
    else:
        return _decode_item(obj)


def _get_all(store: typing.Callable, search_key: str) -> typing.List[typing.Any]:
    """Wraps redis.mget command.
    
    :param store: Cache store connection wrapper.
    :param search_key: Key woth which to search cache.

    :returns: If a key match then collection of decoded domain object(s), else None.

    """
    logger.log(f"CACHE :: get :: {search_key}")
    CHUNK_SIZE = 5000
    _, keys = store.scan(match=search_key, count=CHUNK_SIZE)

    return [_decode_item(i) for i in store.mget(keys)] if keys else []


def _get_count(store: typing.Callable, search_key: str) -> int:
    """Wraps redis.mget command.
    
    :param store: Cache store connection wrapper.
    :param search_key: Key woth which to search cache.

    :returns: If a key match then collection of decoded domain object(s), else None.

    """
    logger.log(f"CACHE :: get_count :: {search_key}")
    CHUNK_SIZE = 5000
    _, keys = store.scan(match=search_key, count=CHUNK_SIZE)

    return len(keys)


def _set(store: typing.Callable, key: str, data: typing.Any) -> str:
    """Wraps redis.set command.
    
    :param store: Cache store connection wrapper.
    :param key: Key of item to be cached.
    :param data: Data to be cached.

    :returns: Cache key.

    """
    logger.log(f"CACHE :: set :: {key}")
    
    store.set(key, json.dumps(encoder.encode(data), indent=4))

    return key


def _setnx(store: typing.Callable, key: str, data: typing.Any) -> typing.Tuple[str, bool]:
    """Wraps redis.setnx command.
    
    :param store: Cache store connection wrapper.
    :param key: Key of item to be cached.
    :param data: Data to be cached.

    :returns: True if .

    """
    logger.log(f"CACHE :: setnx :: {key}")

    return bool(store.setnx(key, json.dumps(encoder.encode(data), indent=4)))
