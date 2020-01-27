import json
import typing

from stests.core.utils import encoder



def do_delete(store: typing.Callable, key: str):
    """Wraps redis.delete command.
    
    :param store: Cache store connection wrapper.
    :param key: Key of item to be uncached.

    """
    store.delete(key)


def do_set(store: typing.Callable, key: str, data: typing.Any):
    """Wraps redis.set command.
    
    :param store: Cache store connection wrapper.
    :param key: Key of item to be cached.
    :param data: Data to be cached.

    """
    store.set(key, json.dumps(encoder.encode(data), indent=4))


def do_get(store: typing.Callable, key: str) -> typing.Any:
    """Wraps redis.get command.
    
    :param store: Cache store connection wrapper.
    :param key: Key of item to be cached.

    """
    return encoder.decode(json.loads(store.get(key)))
