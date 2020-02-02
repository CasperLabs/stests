from stests.core.cache.stores import get_store
from stests.core.cache.utils import do_get
from stests.core.cache.utils import do_set
from stests.core.cache.utils import get_key
from stests.core.types import Account
from stests.core.types import AccountType



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


def set_account(namespace: str, account: Account) -> str:
    """Appends an account to cache store.

    :param namespace: Cache key namespace.
    :param account: Account being cached.

    :returns: Account's cache key.

    """
    # Set keyspace.
    key = get_key(
        f"{namespace}:ACCOUNT.{account.typeof.name}",
        str(account.idx).zfill(7)
        )

    # Push to store.
    with get_store() as store:
        do_set(store, key, account)

    return key
