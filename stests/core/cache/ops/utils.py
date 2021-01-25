import json
import typing
import functools
import time

import redis

from stests.core.cache.model import StoreOperation
from stests.core.cache.model import StorePartition
from stests.core.cache.model import CountDecrementKey
from stests.core.cache.model import CountIncrementKey
from stests.core.cache.model import Item
from stests.core.cache.model import ItemKey
from stests.core.cache.model import SearchKey
from stests.core.cache import stores
from stests.core.utils import encoder



def _decode_item(as_json: str) -> typing.Any:
    """Returns a decoded encached domain object(s).

    """
    if as_json is not None:
        return encoder.decode(json.loads(as_json))


def _decr(store: typing.Callable, decrement: CountDecrementKey):
    """Decrements count under exactly matched key.
    
    """
    store.decrby(decrement.key, decrement.amount)


def _delete_one(store: typing.Callable, item_key: ItemKey):
    """Deletes item under exactly matched key.
    
    """
    store.delete(item_key.key)


def _delete_many(store: typing.Callable, search_key: SearchKey):
    """Deletes items under matching keys.

    """
    chunk_size = 1000
    cursor = '0'
    while cursor != 0:
        cursor, keys = store.scan(cursor=cursor, match=search_key.key, count=chunk_size)
        if keys:
            store.delete(*keys)


def _get_counter_one(store: typing.Callable, item_key: ItemKey) -> int:
    """Returns count under exactly matched key.
    
    """
    count = store.get(item_key.key)

    return 0 if count is None else int(count)


def _get_counter_many(store: typing.Callable, search_key: SearchKey) -> typing.Tuple[typing.List[str], typing.List[int]]:
    """Returns counts under matched keys.
    
    """
    keys = []
    chunk_size = 1000
    cursor = '0'
    while cursor != 0:
        cursor, keys_ = store.scan(cursor=cursor, match=search_key.key, count=chunk_size)
        keys += keys_

    return [i.decode('utf8') for i in keys], [int(i) for i in store.mget(keys)]


def _get_count(store: typing.Callable, search_key: SearchKey) -> int:
    """Returns length of collection under matched keys.
    
    """
    count = 0
    chunk_size = 1000
    cursor = '0'
    while cursor != 0:
        cursor, keys = store.scan(cursor=cursor, match=search_key.key, count=chunk_size)
        count += len(keys)

    return count


def _get_one(store: typing.Callable, item_key: ItemKey) -> typing.Any:
    """Returns item under exactly matched key.
    
    """
    return _decode_item(store.get(item_key.key))


def _get_one_from_many(store: typing.Callable, item_key: ItemKey) -> typing.Any:
    """Returns item under first matched key.
    
    """
    chunk_size = 1000
    cursor = '0'
    while cursor != 0:
        cursor, keys = store.scan(cursor=cursor, match=item_key.key, count=chunk_size)
        if keys:
            return _decode_item(store.get(keys[0]))


def _get_many(store: typing.Callable, search_key: SearchKey) -> typing.List[typing.Any]:
    """Returns collection cached under all matched keys.
    
    """
    keys = []
    chunk_size = 2000
    cursor = '0'
    while cursor != 0:
        cursor, keys_ = store.scan(cursor=cursor, match=search_key.key, count=chunk_size)
        keys += keys_

    return [_decode_item(i) for i in store.mget(keys)] if keys else []


def _incr(store: typing.Callable, item_key: CountIncrementKey) -> typing.Any:
    """Increments count under exactly matched key.
    
    """
    return store.incrby(item_key.key, item_key.amount)


def _set_one(store: typing.Callable, item: Item) -> str:
    """Set item under a key.
    
    """
    store.set(item.key, item.data_as_json, ex=item.expiration)

    return item.key


def _set_one_singleton(store: typing.Callable, item: Item) -> typing.Tuple[str, bool]:
    """Sets item under a key if not already cached.
    
    """
    key, was_cached = item.key, bool(store.setnx(item.key, item.data_as_json))
    if was_cached and item.expiration:
        store.expire(key, item.expiration)

    return key, was_cached  


# Map: operation -> redis command wrapper.
_HANDLERS = {
    StoreOperation.COUNTER_DECR: _decr,
    StoreOperation.DELETE_ONE: _delete_one,
    StoreOperation.DELETE_MANY: _delete_many,
    StoreOperation.GET_COUNT: _get_count,
    StoreOperation.GET_COUNTER_ONE: _get_counter_one,
    StoreOperation.GET_COUNTER_MANY: _get_counter_many,
    StoreOperation.GET_ONE: _get_one,
    StoreOperation.GET_ONE_FROM_MANY: _get_one_from_many,
    StoreOperation.GET_MANY: _get_many,
    StoreOperation.COUNTER_INCR: _incr,
    StoreOperation.SET_ONE: _set_one,
    StoreOperation.SET_ONE_SINGLETON: _set_one_singleton,
}

# Set of partitions whereby keys are prefixed with os-user. 
_USER_PARTITIONS = {
    StorePartition.ORCHESTRATION,
    StorePartition.STATE,
}

# Max. number of times an operation will be tried.
_MAX_OP_ATTEMPTS = 5


def cache_op(partition: StorePartition, operation: StoreOperation) -> typing.Callable:
    """Decorator to orthoganally process a cache operation.

    :param partition: Cache partition to which operation pertains.
    :param operation: Cache operation to apply.

    :returns: Decorated function.
    
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # JIT extend encoder - ensures all types are registered.
            encoder.initialise()
            
            
            with stores.get_store(partition) as store:
                # Invoke inner function.
                obj = func(*args, **kwargs)
                if obj is None:
                    return
                
                # Apply key prefixing.
                if partition in _USER_PARTITIONS:
                    obj.apply_key_prefix()
                
                # Invoke operation applying retry semantics in case of broken pipes.
                # TODO: revisit connection pooling, 
                attempts = 0
                handler = _HANDLERS[operation]
                while attempts < _MAX_OP_ATTEMPTS:
                    try:
                        return handler(store, obj)
                    except redis.ConnectionError as err:
                        attempts += 1
                        if attempts == _MAX_OP_ATTEMPTS:
                            raise err
                        time.sleep(float(0.01))

        return wrapper
    return decorator
