from stests.core.cache.stores import get_store
from stests.core.cache.utils import do_delete
from stests.core.cache.utils import do_get
from stests.core.cache.utils import do_set
from stests.core.types import Network



def get_network(network_id: str) -> Network:
    """Retrieves netowrk information from cache store.

    :param str: ID of network.
    :returns: Cached network information.

    """    
    # Set key.
    key = network_id

    # Pull from store.
    with get_store(network_id) as store:
        return do_get(store, key)


def set_network(network: Network) -> str:
    """Appends network information to cache store.

    :param ctx: Contextual information passed along the flow of execution.
    :param network: Network information being cached.

    :returns: Network's cache key.

    """
    # Set key.
    key = network.name

    # Push to store.
    with get_store(network.name) as store:
        do_delete(store, key)
        do_set(store, key, network)

    return key
