import typing

from stests.core import cache
from stests.core import factory
from stests.core.types.orchestration import ExecutionContext
from stests.generators.utils import accounts
from stests.generators.utils import constants
from stests.generators.utils import verification



# Step label.
LABEL = "create-accounts"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    def _yield_accounts() -> typing.Generator:
        yield factory.create_account_for_run(
            ctx,
            accounts.get_account_idx_for_run_faucet(ctx.args.accounts, ctx.args.transfers)
            )
        for account_index in accounts.get_account_range(ctx.args.accounts, ctx.args.transfers):
            yield factory.create_account_for_run(ctx, account_index)
        
    for account in _yield_accounts():
        cache.state.set_account(account)
