from stests.core.cache.stores import get_store
from stests.core.cache.utils import do_get
from stests.core.cache.utils import do_set
from stests.core.types import Node



def get_node(network_id: str, node_id: str) -> Node:
    """Retrieves node information from cache store.

    :param str: ID of network.
    :returns: Cached network information.

    """    
    # Set key.
    key = network_id

    # Pull from store.
    with get_store() as store:
        return do_get(store, key)


def set_node(node: Node):
    """Appends node information to cache store.

    :param node: Node information being cached.

    """    
    with get_store() as store:
        do_set(store, node.cache_key, node)
