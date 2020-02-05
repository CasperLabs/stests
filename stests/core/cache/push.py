from stests.core.cache.stores import get_store
from stests.core.cache.utils import do_set
from stests.core.utils import encoder




def _set_instance(instance):
    """Sink function to push instances of domain types.
    
    """
    if type(instance) not in encoder.TYPESET:
        raise TypeError("Instance to be cached is not a domain type.")

    with get_store() as store:
        do_set(store, instance.cache_key, instance)


# Append account information.
set_account = _set_instance


# Append network information.
set_network = _set_instance


# Append node information.
set_node = _set_instance


# Append run information.
set_run = _set_instance
