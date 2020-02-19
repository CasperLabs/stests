import random
import typing

from stests.core.cache.utils import decache
from stests.core.cache.identifiers import AccountIdentifier
from stests.core.domain import Account
from stests.core.domain import RunContext
from stests.core.utils import factory



@decache
def get_account(account_id: AccountIdentifier) -> Account:
    """Decaches domain object: Account.
    
    """
    run = account_id.run

    return [
        "run-account",
        run.network.name,
        run.type,
        f"R-{str(run.index).zfill(3)}",
        f"{str(account_id.index).zfill(6)}"
    ]


def get_account_by_ctx(ctx: RunContext, index: int) -> Account:
    """Decaches domain object: Account.
    
    """
    account_id = factory.create_account_id(
        index,
        ctx.network_name,
        ctx.run_index,
        ctx.run_type
        )

    return get_account(account_id)
