import json
import typing
import dataclasses
import functools

from stests.core.cache.enums import StoreOperation
from stests.core.cache.enums import StorePartition
from stests.core.cache import stores
from stests.core.utils import encoder
from stests.core.utils import logger



def cache_op(partition: StorePartition, operation: StoreOperation):
    """Decorator to orthoganally process a cache operation.

    :param on_success: Continuation function upon execution success.
    :param is_substep: Flag indicating whether decorated function is a sub-step or not.

    :returns: Decorated function.
    
    """
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            with stores.get_store(partition) as store:

                if operation == StoreOperation.FLUSH:
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

                elif operation == StoreOperation.INCR:
                    keypath = func(*args, **kwargs)
                    key = ":".join([str(i) for i in keypath])
                    store.incrby(key, 1)

                elif operation == StoreOperation.LOCK:
                    keypath, data = func(*args, **kwargs)
                    key = ":".join([str(i) for i in keypath])
                    data = dataclasses.asdict(data)
                    return key, _setnx(store, key, data)

                elif operation == StoreOperation.SET:
                    keypath, data = func(*args, **kwargs)
                    key = ":".join([str(i) for i in keypath])
                    _set(store, key, data)
                    return key

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
    return encoder.decode(json.loads(as_json))
    

def _delete(store: typing.Callable, key: str):
    """Wraps redis.delete command.
    
    """
    logger.log(f"CACHE :: delete :: {key}")
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
    logger.log(f"CACHE :: get :: {key}")
    obj = store.get(key)
    if obj is None:
        logger.log_warning(f"CACHE :: get :: {key} :: not found")
    else:
        return _decode_item(obj)


def _get_all(store: typing.Callable, search_key: str) -> typing.List[typing.Any]:
    """Wraps redis.mget command.
    
    """
    logger.log(f"CACHE :: get :: {search_key}")
    CHUNK_SIZE = 5000
    _, keys = store.scan(match=search_key, count=CHUNK_SIZE)

    return [_decode_item(i) for i in store.mget(keys)] if keys else []


def _get_count(store: typing.Callable, search_key: str) -> int:
    """Wraps redis.mget command.
    
    """
    logger.log(f"CACHE :: get_count :: {search_key}")
    CHUNK_SIZE = 5000
    _, keys = store.scan(match=search_key, count=CHUNK_SIZE)

    return len(keys)


def _set(store: typing.Callable, key: str, data: typing.Any) -> str:
    """Wraps redis.set command.
    
    """
    logger.log(f"CACHE :: set :: {key}")
    
    store.set(key, json.dumps(encoder.encode(data), indent=4))

    return key


def _setnx(store: typing.Callable, key: str, data: typing.Any) -> typing.Tuple[str, bool]:
    """Wraps redis.setnx command.
    
    """
    logger.log(f"CACHE :: setnx :: {key}")

    return bool(store.setnx(key, json.dumps(encoder.encode(data), indent=4)))
