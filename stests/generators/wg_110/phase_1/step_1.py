import typing
import dramatiq

from stests.core.types.chain import DeployType
from stests.core.types.orchestration import ExecutionContext
from stests.generators.utils import constants
from stests.generators.utils import verification
from stests.generators.utils.accounts import do_transfer



# Step label.
LABEL = "do-transfers"

def execute(ctx: ExecutionContext) -> typing.Union[dramatiq.Actor, int, typing.Callable]:
    """Step entry point.
    
    :param ctx: Execution context information.

    :returns: 3 member tuple -> actor, message count, message arg factory.

    """
    def _yield_parameterizations() -> typing.Generator:
        for account_index in range(1, ctx.args.transfers + 1):
            yield (
                ctx,
                constants.ACC_NETWORK_FAUCET,
                account_index,
                ctx.args.amount,
                DeployType.TRANSFER_WASM,
            )

    return do_transfer, ctx.args.transfers, _yield_parameterizations


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    verification.verify_deploy_count(ctx, ctx.args.transfers) 