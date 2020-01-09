import redis

from stests.core.cache.stores.redis.connection import get_connection



def get_store(network_id: str = None) -> redis.Redis:
    """Returns instance of a redis cache store accessor.

    :param network_id: Network identifier, e.g. LOC-DEV-01
    :returns: An instance of a redis cache store accessor.

    """
    # TODO: map network id to a redis db so as to partition when
    #       running tests across multiple networks.
    db = 1

    return get_connection(db)
