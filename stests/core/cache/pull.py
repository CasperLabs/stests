from stests.core.cache.push import set_network
from stests.core.cache.stores import get_store
from stests.core.cache.utils import do_get
from stests.core.cache.utils import do_set
from stests.core.cache.utils import get_key

from stests.core.types import Account
from stests.core.types import AccountType
from stests.core.types import Node
from stests.core.types import Network



def get_account(
    network_id: str,
    namespace: str,
    typeof: AccountType,
    index: int
    ) -> Account:
    """Retrieves an account from cache store.

    :param network_id: Identifier of network being tested.
    :param namespace: Cache key namespace.
    :param typeof: Type of account to be retrieved.
    :param index: Index of account.
    :returns: A previously cached account.

    """    
    # Set keyspace.
    namespace = f"{namespace}.account.{str(typeof).split('.')[-1]}"
    key = get_key(network_id, namespace, str(index).zfill(7))

    # Pull from store.
    with get_store() as store:
        return do_get(store, key)


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