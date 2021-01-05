import typing

from stests.core.types.chain import DeployType
from stests.core.types.orchestration import ExecutionContext
from stests.generators.utils import accounts
from stests.generators.utils import constants
from stests.generators.utils import verification



# Step label.
LABEL = "do-transfers"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.
    :returns: 3 member tuple -> actor, message count, message arg factory.

    """
    def _yield_parameterizations() -> typing.Generator:
        account_range = range(1, ctx.args.transfers + 1)
        for account_index in account_range:
            yield (
                ctx,
                constants.ACC_NETWORK_FAUCET,
                account_index,
                ctx.args.amount,
                DeployType.TRANSFER_NATIVE,
            )

    return accounts.do_transfer_fire_forget, ctx.args.transfers, _yield_parameterizations    


def verify(ctx: ExecutionContext):
    """Step execution verifier.
    
    :param ctx: Execution context information.

    """
    print("TODO: verify cached account count")
