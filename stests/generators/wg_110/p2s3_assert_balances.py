import typing

from stests import chain
from stests.core import cache
from stests.core import factory
from stests.core.types.orchestration import ExecutionContext
from stests.generators.utils import accounts
from stests.generators.utils import constants
from stests.generators.utils import verification



# Step label.
LABEL = "assert-balances"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    for account_idx in accounts.get_account_range(ctx.args.accounts, ctx.args.transfers):
        transfers = accounts.get_account_deploy_count(ctx.args.accounts, account_idx, ctx.args.transfers)
        amount = transfers * (ctx.args.amount + chain.DEFAULT_TX_FEE_NATIVE_TRANSFER)
        verification.verify_account_balance(ctx, account_idx, amount)
