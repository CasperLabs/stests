from stests.core.cache.stores import get_store
from stests.core.cache.utils import do_get
from stests.core.cache.utils import do_set
from stests.core.cache.utils import get_key
from stests.core.types import Account
from stests.core.types import AccountType



def delete_run_data(
    network_id: str,
    namespace: str,
    typeof: AccountType,
    index: int
    ) -> Account:
    """Deletes all data related to a generator run.


    """    
    print(107)

    # Set keyspace.
    # namespace = f"{namespace}.account.{str(typeof).split('.')[-1]}"
    # key = get_key(network_id, namespace, str(index).zfill(7))

    # # Pull from store.
    # with get_store() as store:
    #     return do_get(store, key)
