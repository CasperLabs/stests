from stests.core.cache.push import set_network
from stests.core.cache.stores import get_store
from stests.core.cache.utils import do_get
from stests.core.cache.utils import do_set
from stests.core.cache.utils import get_key

from stests.core.types import Account
from stests.core.types import AccountType
from stests.core.types import Node
from stests.core.types import Network
from stests.core.types import NetworkIdentifier



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


# Get account information.
get_account = _do_get


# Get network information.
get_network = _do_get


# Get node information.
get_node = _do_get


# Get node information.
get_run = _do_get
