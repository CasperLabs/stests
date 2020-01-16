from stests.core.types import Account
from stests.core.types import AccountType
from stests.core.cache.utils.commands import do_set
from stests.core.cache.utils.commands import do_get
from stests.core.cache.utils.keyspace import get_key
from stests.core.utils.execution import ExecutionContext



def append_account(ctx: ExecutionContext, account: Account) -> str:
    """Appends an account to cache store.

    :param ctx: Contextual information passed along the flow of execution.
    :param account: Account being cached.

    :returns: Account's cache key.

    """
    # Set key.
    key = get_key(ctx, f"account.{account.short_type}", _get_index(account.index))

    # Push to store.
    do_set(ctx, key, account)

    return key


def retrieve_account(ctx: ExecutionContext, typeof: AccountType, index: int) -> Account:
    """Retrieves an account from cache store.

    :param ctx: Contextual information passed along the flow of execution.
    :param typeof: Type of account to be retrieved.
    :param index: Index of account.

    :returns: A previously cached account.

    """    
    # Set key.
    key = get_key(ctx, f"account.{str(typeof).split('.')[-1]}", _get_index(index))

    # Pull from store.
    return do_get(ctx, key)


def _get_index(index):
    """Returns an account index formatted for key usage.
    
    """
    return str(index).zfill(7)
