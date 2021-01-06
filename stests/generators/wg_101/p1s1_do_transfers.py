import typing

from stests.core.types.chain import DeployType
from stests.core.types.orchestration import ExecutionContext
from stests.generators.utils import accounts
from stests.generators.utils import constants



# Step label.
LABEL = "do-transfers"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.
    :returns: 3 member tuple -> actor, message count, message arg factory.

    """
    accounts.do_transfer_fire_forget(
        ctx,
        constants.ACC_NETWORK_FAUCET,
        range(1, ctx.args.transfers + 1),
        ctx.args.amount,
        DeployType.TRANSFER_NATIVE,
        )    
