from stests.core.cache.utils.commands import do_set
from stests.core.cache.utils.keyspace import get_key
from stests.core.types.account import Account
from stests.core.utils.execution import ExecutionContext



def append(ctx: ExecutionContext, account: Account) -> str:
    """Appends an account to cache store.

    :param ctx: Contextual information passed along the flow of execution.
    :param account: Account being cached.

    :returns: Account's cache key.

    """
    # Set key.
    key = get_key(ctx, f"account.{account.short_type}", account.index)

    # Push to store.
    do_set(ctx, key, account)

    return key


# def retrieve_user(ctx: ExecutionContext, index: int):
#     pass


# def retrieve_contract(ctx: ExecutionContext, index: int):
#     pass
