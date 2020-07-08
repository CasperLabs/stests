import typing

from stests.core import cache
from stests.core import factory
from stests.core.types.chain import AccountType
from stests.core.types.orchestration import ExecutionContext
from stests.orchestration.generators.utils import constants
from stests.orchestration.generators.utils import verification



# Step label.
LABEL = "create-accounts"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    for account_index, account_type in _yield_accounts(ctx):
        cache.state.set_account(factory.create_account_for_run(
            ctx,
            index=account_index,
            typeof=account_type,
        ))


def _yield_accounts(ctx: ExecutionContext) -> typing.Generator:
    """Yields account information to be persisted to cache.
    
    """
    yield constants.ACC_RUN_FAUCET, AccountType.FAUCET
    yield constants.ACC_RUN_CONTRACT, AccountType.CONTRACT
    for index in range(constants.ACC_RUN_USERS, ctx.args.user_accounts + constants.ACC_RUN_USERS):
        yield index, AccountType.USER


def verify(ctx: ExecutionContext):
    """Step execution verifier.
    
    :param ctx: Execution context information.

    """
    pass