from stests.core.cache.stores import get_store
from stests.core.cache.utils import do_set
from stests.core.types import CLASSES


from stests.core.types import Account
from stests.core.types import AccountType


def _set_domain_type_instance(instance):
    """Sink function to push instances of domain types.
    
    """
    if type(instance) not in CLASSES:
        raise TypeError("Instance to be cached is not a domain type.")

    print(666, instance.cache_key)

    with get_store() as store:
        do_set(store, instance.cache_key, instance)


# Append account information.
set_account = lambda i: _set_domain_type_instance(i)


# Append network information.
set_network = lambda i: _set_domain_type_instance(i)


# Append node information.
set_node = lambda i: _set_domain_type_instance(i)
