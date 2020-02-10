from stests.core.cache import keyspace
from stests.core.cache import stores
from stests.core.cache import utils



def _do_set(instance):
    """Sink function to push instances of domain types.
    
    """
    key = keyspace.get_key(instance)
    with stores.get_store() as store:
        utils.do_set(store, key, instance)


# Append account information.
set_account = _do_set


# Append network information.
set_network = _do_set


# Append node information.
set_node = _do_set


# Append run context information.
set_run_context = _do_set


# Append run event information.
set_run_event = _do_set
