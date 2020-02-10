from stests.core.cache import keyspace
from stests.core.cache import stores
from stests.core.cache import utils



def _do_get(key_ref):
    """Sink function to retrieve instances of domain types.
    
    """
    key = keyspace.get_key(key_ref)
    with stores.get_store() as store:
        return utils.do_get(store, key)


# Get account information.
get_account = _do_get


# Get network information.
get_network = _do_get


# Get node information.
get_node = _do_get


# Get node information.
get_run = _do_get
