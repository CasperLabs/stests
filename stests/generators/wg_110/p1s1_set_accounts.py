import typing

from stests.core import cache
from stests.core import factory
from stests.core.types.orchestration import ExecutionContext
from stests.generators.utils import constants
from stests.generators.utils import verification



# Step label.
LABEL = "create-accounts"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    for account in _yield_accounts(ctx):
        cache.state.set_account(account)


def _yield_accounts(ctx: ExecutionContext) -> typing.Generator:
    """Yields account information to be persisted to cache.
    
    """
    # Run faucet account.
    yield factory.create_account_for_run(ctx, constants.ACC_RUN_FAUCET)
    
    # User accounts.
    account_range = range(constants.ACC_RUN_USERS, ctx.args.transfers + constants.ACC_RUN_USERS)
    for account_index in account_range:
        yield factory.create_account_for_run(ctx, account_index)


def verify(ctx: ExecutionContext):
    """Step execution verifier.
    
    :param ctx: Execution context information.

    """
    print("TODO: verify cached account count")
