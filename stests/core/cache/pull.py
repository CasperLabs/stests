from stests.core.cache.push import set_network
from stests.core.cache.stores import get_store
from stests.core.cache.utils import do_get
from stests.core.cache.utils import do_set
from stests.core.cache.utils import get_key

from stests.core.types import Account
from stests.core.types import AccountType
from stests.core.types import Node
from stests.core.types import Network
from stests.core.types import NetworkReference



def _do_get(key_ref):
    """Sink function to retrieve instances of domain types.
    
    """
    # Parse key.
    try:
        key_ref.cache_key
    except AttributeError:
        key = key_ref
    else:
        key = key_ref.cache_key

    # Return cache contents.
    with get_store() as store:
        return do_get(store, key)


# Get network information.
get_network = _do_get


# Get node information.
get_node = _do_get




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
