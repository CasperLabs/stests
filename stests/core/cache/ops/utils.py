import json
import typing
import dataclasses
import functools

from stests.core.cache.model import StoreOperation
from stests.core.cache.model import StorePartition
from stests.core.cache.model import CacheIncrementKey
from stests.core.cache.model import CacheItem
from stests.core.cache.model import CacheItemKey
from stests.core.cache.model import CacheSearchKey
from stests.core.cache import stores
from stests.core.utils import encoder



def _decode_item(as_json: str) -> typing.Any:
    """Returns a decoded encached domain object(s).

    """
    if as_json is not None:
        return encoder.decode(json.loads(as_json))
    

def _delete_one(store: typing.Callable, ik: CacheItemKey):
    """Wraps redis.delete command.
    
    """
    store.delete(ik.key)


def _flush_many(store: typing.Callable, sk: CacheSearchKey):
    """Flushes data from cache.

    """
    CHUNK_SIZE = 1000
    cursor = '0'
    while cursor != 0:
        cursor, keys = store.scan(cursor=cursor, match=sk.key, count=CHUNK_SIZE)
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


def _get_one_from_many(store: typing.Callable, ik: CacheItemKey) -> typing.Any:
    """Wraps redis.get command.
    
    """
    many = _get_many(store, ik)

    return many[0] if many else None


def _get_count_one(store: typing.Callable, ik: CacheItemKey) -> int:
    """Wraps redis.get command.
    
    """
    return int(store.get(ik.key))


def _get_count_many(store: typing.Callable, sk: CacheSearchKey) -> typing.List[typing.Any]:
    """Wraps redis.mget command.
    
    """
    CHUNK_SIZE = 5000
    _, keys = store.scan(match=sk.key, count=CHUNK_SIZE)
    counts = [int(i) for i in store.mget(keys)]

    return [i.decode('utf8') for i in keys], counts


def _get_many(store: typing.Callable, sk: CacheSearchKey) -> typing.List[typing.Any]:
    """Wraps redis.mget command.
    
    """
    CHUNK_SIZE = 5000
    _, keys = store.scan(match=sk.key, count=CHUNK_SIZE)

    return [_decode_item(i) for i in store.mget(keys)] if keys else []


def _incr_one(store: typing.Callable, ik: CacheIncrementKey) -> typing.Any:
    """Wraps redis.incrby command.
    
    """
    return store.incrby(ik.key, ik.amount)


def _set_one(store: typing.Callable, item: CacheItem) -> str:
    """Wraps redis.set command.
    
    """
    store.set(item.key, item.data_as_json)

    return item.key


def _set_one_singleton(store: typing.Callable, item: CacheItem) -> typing.Tuple[str, bool]:
    """Wraps redis.setnx command.
    
    """
    was_cached = bool(store.setnx(item.key, item.data_as_json))

    return item.key, was_cached


def _get_all(store: typing.Callable, search_key: str) -> typing.List[typing.Any]:
    """Wraps redis.mget command.
    
    """
    CHUNK_SIZE = 5000
    _, keys = store.scan(match=search_key, count=CHUNK_SIZE)

    return [_decode_item(i) for i in store.mget(keys)] if keys else []


def _get_count_matched(store: typing.Callable, search_key: str) -> typing.List[typing.Any]:
    """Wraps redis.mget command.
    
    """
    CHUNK_SIZE = 5000
    _, keys = store.scan(match=search_key, count=CHUNK_SIZE)

    return len(keys)


def _set(store: typing.Callable, key: str, data: typing.Any) -> str:
    """Wraps redis.set command.
    
    """
    store.set(key, json.dumps(encoder.encode(data), indent=4))

    return key


def _setnx(store: typing.Callable, key: str, data: typing.Any) -> typing.Tuple[str, bool]:
    """Wraps redis.setnx command.
    
    """
    return bool(store.setnx(key, json.dumps(encoder.encode(data), indent=4)))


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

                if operation == StoreOperation.DECR_ONE:
                    keypath, amount = func(*args, **kwargs)
                    key = ":".join([str(i) for i in keypath])
                    return store.decrby(key, amount)

                elif operation == StoreOperation.DELETE_ONE:
                    _delete_one(store, func(*args, **kwargs))

                elif operation == StoreOperation.FLUSH_MANY:
                    _flush_many(store, func(*args, **kwargs))

                elif operation == StoreOperation.GET_COUNT_ONE:
                    return _get_count_one(store, func(*args, **kwargs))

                elif operation == StoreOperation.GET_COUNT_MANY:
                    return _get_count_many(store, func(*args, **kwargs))

                elif operation == StoreOperation.GET_COUNT_MATCHED:
                    keypath = func(*args, **kwargs)
                    key = ":".join([str(i) for i in keypath])
                    return _get_count_matched(store, key)

                elif operation == StoreOperation.GET_ONE:
                    return _get_one(store, func(*args, **kwargs))

                elif operation == StoreOperation.GET_ONE_FROM_MANY:
                    return _get_one_from_many(store, func(*args, **kwargs))

                elif operation == StoreOperation.GET_MANY:
                    return _get_many(store, func(*args, **kwargs))

                elif operation == StoreOperation.INCR_ONE:
                    return _incr_one(store, func(*args, **kwargs))

                elif operation == StoreOperation.LOCK_ONE:
                    return _set_one_singleton(store, func(*args, **kwargs))

                elif operation == StoreOperation.SET:
                    return _set_one(store, func(*args, **kwargs))

                elif operation == StoreOperation.SET_ONE:
                    return _set_one(store, func(*args, **kwargs))

                elif operation == StoreOperation.SET_ONE_SINGLETON:
                    return _set_one_singleton(store, func(*args, **kwargs))

                else:
                    raise NotImplementedError("Cache operation is unsupported")

        return wrapper

    return decorator
