import json
import typing
import dataclasses
import functools

from stests.core.cache.model import StoreOperation
from stests.core.cache.model import StorePartition
from stests.core.cache.model import CacheItem
from stests.core.cache.model import CacheItemKey
from stests.core.cache.model import CacheSearchKey
from stests.core.cache import stores
from stests.core.utils import encoder



def cache_op(partition: StorePartition, operation: StoreOperation) -> typing.Callable:
    """Decorator to orthoganally process a cache operation.

    :param partition: Cache partition to which operation pertains.
    :param operation: Cache operation to apply.

    :returns: Decorated function.
    
    """
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            # JIT iniitalise encoder to ensure all types are registered.
            encoder.initialise()

            with stores.get_store(partition) as store:

                if operation == StoreOperation.DECR:
                    keypath, amount = func(*args, **kwargs)
                    key = ":".join([str(i) for i in keypath])
                    return store.decrby(key, amount)

                elif operation == StoreOperation.DELETE:
                    keypath = func(*args, **kwargs)
                    key = ":".join([str(i) for i in keypath])
                    _delete(store, key)

                elif operation == StoreOperation.FLUSH:
                    for keypaths in func(*args, **kwargs):
                        key = ":".join([str(i) for i in keypaths])
                        _flush(store, key)

                elif operation == StoreOperation.GET:
                    keypath = func(*args, **kwargs)
                    key = ":".join([str(i) for i in keypath])
                    if key.find("*") >= 0:
                        return _get_all(store, key)
                    else:
                        return _get(store, key)

                elif operation == StoreOperation.GET_COUNT:
                    keypath = func(*args, **kwargs)
                    key = ":".join([str(i) for i in keypath])
                    return int(store.get(key))

                elif operation == StoreOperation.GET_COUNTS:
                    keypath = func(*args, **kwargs)
                    key = ":".join([str(i) for i in keypath])
                    return _get_all_counts(store, key)

                elif operation == StoreOperation.GET_COUNT_MATCHED:
                    keypath = func(*args, **kwargs)
                    key = ":".join([str(i) for i in keypath])
                    return _get_count_matched(store, key)

                elif operation == StoreOperation.GET_ONE:
                    return _get_one(store, func(*args, **kwargs))

                elif operation == StoreOperation.GET_MANY:
                    return _get_many(store, func(*args, **kwargs))

                elif operation == StoreOperation.INCR:
                    keypath, amount = func(*args, **kwargs)
                    key = ":".join([str(i) for i in keypath])
                    return store.incrby(key, amount)

                elif operation == StoreOperation.LOCK:
                    keypath, data = func(*args, **kwargs)
                    key = ":".join([str(i) for i in keypath])
                    return key, _setnx(store, key, data)

                elif operation == StoreOperation.SET:
                    return _set_one(store, func(*args, **kwargs))

                elif operation == StoreOperation.SET_SINGLETON:
                    keypath, data = func(*args, **kwargs)
                    key = ":".join([str(i) for i in keypath])
                    was_cached = _setnx(store, key, data)
                    return key, was_cached

                else:
                    raise NotImplementedError("Cache operation is unsupported")

        return wrapper

    return decorator


def _decode_item(as_json: str) -> typing.Any:
    """Returns a decoded encached domain object(s).

    """
    if as_json is not None:
        return encoder.decode(json.loads(as_json))
    

def _delete(store: typing.Callable, key: str):
    """Wraps redis.delete command.
    
    """
    store.delete(key)


def _flush(store: typing.Callable, ns_keys: str):
    """Flushes data from cache.

    """
    CHUNK_SIZE = 1000
    cursor = '0'
    while cursor != 0:
        cursor, keys = store.scan(cursor=cursor, match=ns_keys, count=CHUNK_SIZE)
        if keys:
            store.delete(*keys)


def _get(store: typing.Callable, key: str) -> typing.Any:
    """Wraps redis.get command.
    
    """
    obj = store.get(key)
    if obj is not None:
        return _decode_item(obj)


def _get_one(store: typing.Callable, ik: CacheItemKey) -> typing.Any:
    """Wraps redis.get command.
    
    """
    return _decode_item(store.get(ik.key))


def _get_many(store: typing.Callable, sk: CacheSearchKey) -> typing.List[typing.Any]:
    """Wraps redis.mget command.
    
    """
    CHUNK_SIZE = 5000
    _, keys = store.scan(match=sk.key, count=CHUNK_SIZE)

    return [_decode_item(i) for i in store.mget(keys)] if keys else []


def _get_all(store: typing.Callable, search_key: str) -> typing.List[typing.Any]:
    """Wraps redis.mget command.
    
    """
    CHUNK_SIZE = 5000
    _, keys = store.scan(match=search_key, count=CHUNK_SIZE)

    return [_decode_item(i) for i in store.mget(keys)] if keys else []


def _get_all_counts(store: typing.Callable, search_key: str) -> typing.List[typing.Any]:
    """Wraps redis.mget command.
    
    """
    CHUNK_SIZE = 5000
    _, keys = store.scan(match=search_key, count=CHUNK_SIZE)
    counts = [int(i) for i in store.mget(keys)]

    return [i.decode('utf8') for i in keys], counts


def _get_count_matched(store: typing.Callable, search_key: str) -> typing.List[typing.Any]:
    """Wraps redis.mget command.
    
    """
    CHUNK_SIZE = 5000
    _, keys = store.scan(match=search_key, count=CHUNK_SIZE)

    return len(keys)


def _set_one(store: typing.Callable, item: CacheItem) -> str:
    """Wraps redis.set command.
    
    """
    store.set(item.key, item.data_as_json)

    return item.key


def _set(store: typing.Callable, key: str, data: typing.Any) -> str:
    """Wraps redis.set command.
    
    """
    store.set(key, json.dumps(encoder.encode(data), indent=4))

    return key


def _setnx(store: typing.Callable, key: str, data: typing.Any) -> typing.Tuple[str, bool]:
    """Wraps redis.setnx command.
    
    """
    return bool(store.setnx(key, json.dumps(encoder.encode(data), indent=4)))
