from enum import Enum

from stests.core.cache.stores import redis
from stests.core.cache.stores import stub



# Enum: set of supported cache store types.
StoreType = Enum("StoreType", [
    "REDIS",
    "STUB"
])

# Map: Cache store type -> factory.
FACTORIES = {
    StoreType.REDIS: redis,
    StoreType.STUB: stub
}


def get_store(network_id: str, store_type: StoreType = StoreType.REDIS):
    """Returns a cache store ready to be used as a state persistence & flow control mechanism.

    :param network_id: Identifier of network being tested.
    :param store_type: Type of store to be instantiated.
    :returns: A cache store.

    """
    try:
        factory = FACTORIES[store_type]
    except KeyError:
        raise NotImplementedError(f"{store_type} cache store is unsupported")

    return factory.get_store(network_id.upper())
