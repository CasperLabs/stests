from stests.core.cache.stores import redis
from stests.core.cache.stores import stub
from stests.core.utils import env
from stests.core.utils.exceptions import InvalidEnvironmentVariable



# Name of environment variable for deriving cache store type.
EVAR_STORE_TYPE = "CACHE_STORE_TYPE"

# Default type of message broker to instantiate.
DEFAULT_STORE_TYPE = "REDIS"

# Map: Cache store type -> factory.
FACTORIES = {
    "REDIS": redis,
    "STUB": stub
}


def get_store(network_id: str):
    """Returns a cache store ready to be used as a state persistence & flow control mechanism.

    :param network_id: Identifier of network being tested.
    :param store_type: Type of store to be instantiated.
    :returns: A cache store.

    """ 
    factory = FACTORIES[_get_store_type()]

    return factory.get_store(network_id.upper())


def _get_store_type():
    """Interrogates environment variable to derive type of cache store to instantiate.
    
    """    
    val = env.get_var(EVAR_STORE_TYPE)
    if val is None:
        return DEFAULT_STORE_TYPE

    if val not in FACTORIES:
        name = env.get_var_name(EVAR_STORE_TYPE)
        raise InvalidEnvironmentVariable(name, val, FACTORIES)

    return val
