from enum import Enum

from stests.core.cache import redis

# Enum: set of supported cache store types.
CacheTypeEnum = Enum("CacheTypeEnum", "redis memory")

# Map: Cache store type -> store.
STORES = {
    CacheTypeEnum.redis: redis,
    CacheTypeEnum.memory: None
}



def get_store(store_type: CacheTypeEnum = CacheTypeEnum.redis):
    """Returns a cache store used to cache system state in between actor invocations.

    """
    try:
        store = STORES[store_type]
    except KeyError:
        raise NotImplementedError(f"{store_type} cache store is unsupported")

    return store
