import typing

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
    for deploy_idx in range(1, ctx.args.transfers + 1):  
        accounts.do_transfer_fire_forget(
            ctx,
            accounts.get_account_idx_for_network_faucet(),
            accounts.get_account_idx_for_deploy(ctx.args.accounts, deploy_idx),
            ctx.args.amount,
            DeployType.TRANSFER_WASM,
        )
