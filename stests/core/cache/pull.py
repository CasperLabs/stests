from stests.core.cache.push import set_network
from stests.core.cache.stores import get_store
from stests.core.cache.utils import do_get
from stests.core.cache.utils import do_set
from stests.core.cache.keys import get_key

from stests.core.types import Account
from stests.core.types import AccountType
from stests.core.types import Node
from stests.core.types import Network
from stests.core.types import NetworkIdentifier



def _do_get(key_ref):
    """Sink function to retrieve instances of domain types.
    
    """
    with get_store() as store:
        if hasattr(key_ref, 'cache_key'):
            return do_get(store, key_ref.cache_key)
        else:
            return do_get(store, get_key(key_ref))


# Get account information.
get_account = _do_get


# Get network information.
get_network = _do_get


# Get node information.
get_node = _do_get


# Get node information.
get_run = _do_get
