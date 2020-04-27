import fakeredis

from stests.core.cache.model import StorePartition


# Factory simply instantiates an instance.
get_store = fakeredis.FakeStrictRedis



def get_store(_: StorePartition) -> fakeredis.FakeStrictRedis:
    """Returns instance of a fake redis cache store accessor.

    :returns: An instance of a fake redis cache store accessor.

    """
    return fakeredis.FakeStrictRedis()
