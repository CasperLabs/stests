import typing

from stests.core import factory
from stests.core.types.chain import DeployType
from stests.core.types.orchestration import ExecutionContext
from stests.generators.utils import accounts



# Step label.
LABEL = "do-transfers"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.
    :returns: 3 member tuple -> actor, message count, message arg factory.

    """
    account_set = accounts.get_account_set(ctx, ctx.args.accounts, ctx.args.transfers)
    for deploy_idx in range(1, ctx.args.transfers + 1):  
        account_idx = accounts.get_account_idx_for_deploy(ctx.args.accounts, deploy_idx)
        accounts.do_transfer_fire_forget(
            ctx,
            account_set[account_idx - 1],
            ctx.args.amount,
            DeployType.TRANSFER_NATIVE,
        )
