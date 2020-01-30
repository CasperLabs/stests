import json
import typing

from stests.core.utils import encoder
from stests.core.utils import logger



def do_delete(store: typing.Callable, key: str):
    """Wraps redis.delete command.
    
    :param store: Cache store connection wrapper.
    :param key: Key of item to be uncached.

    """
    logger.log(f"CACHE :: delete :: {key}")
    store.delete(key)


def do_set(store: typing.Callable, key: str, data: typing.Any):
    """Wraps redis.set command.
    
    :param store: Cache store connection wrapper.
    :param key: Key of item to be cached.
    :param data: Data to be cached.

    """
    logger.log(f"CACHE :: set :: {key}")
    store.set(key, json.dumps(encoder.encode(data), indent=4))


def do_get(store: typing.Callable, key: str) -> typing.Any:
    """Wraps redis.get command.
    
    :param store: Cache store connection wrapper.
    :param key: Key of item to be cached.

    """
    logger.log(f"CACHE :: get :: {key}")
    print(store.get(key))
    return encoder.decode(json.loads(store.get(key)))


def get_key(network_id: str, namespace: str, item_key: str) -> str:
    """Returns fully qualified cache key.
    
    :param network_id: Identifier of network being tested.
    :param namespace: Namespace to prefix key with.
    :param item_key: Key of item being cached.

    :returns: A fully qualified cache key.

    """
    return f"{network_id}.{namespace}:{item_key}"
