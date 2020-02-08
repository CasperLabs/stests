from stests.core.cache.stores import get_store
from stests.core.cache.utils import do_set
from stests.core.cache.keys import get_key



def _do_set(instance):
    """Sink function to push instances of domain types.
    
    """
    with get_store() as store:
        if hasattr(instance, "cache_key"):
            do_set(store, instance.cache_key, instance)
        else:
            do_set(store, get_key(instance), instance)


# Append account information.
set_account = _do_set


# Append network information.
set_network = _do_set


# Append node information.
set_node = _do_set


# Append run information.
set_run = _do_set

# Append run status information.
set_run_status = _do_set
