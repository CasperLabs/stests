from stests.core.cache.stores import get_store
from stests.core.cache.utils import do_get
from stests.core.cache.utils import do_set
from stests.core.types import Network

from stests.core.cache.push import set_network


def get_network(network_key: str) -> Network:
    """Retrieves network information from cache store.

    :param network_key: Network's key.
    :returns: Cached network information.

    """    
    # Set cache key.
    key = f"{network_key}"

    # Pull from store.
    with get_store() as store:
        return do_get(store, key)


# def set_network(network: Network) -> str:
#     """Appends network information to cache store.

#     :param network: Network information being cached.
#     :returns: Network's cache key.

#     """
#     with get_store() as store:
#         do_set(store, network.cache_key, network)
