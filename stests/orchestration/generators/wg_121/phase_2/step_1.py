import time
import typing

import dramatiq

from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.orchestration.generators.utils import constants
from stests.orchestration.generators.utils import verification
from stests.orchestration.generators.utils.accounts import do_transfer_lite



# Step label.
LABEL = "refund-run-faucet"


def execute(ctx: ExecutionContext) -> typing.Union[dramatiq.Actor, int, typing.Callable]:
    """Step entry point.
    
    :param ctx: Execution context information.

    :returns: 3 member tuple -> actor, message count, message arg factory.

    """
    time.sleep(float(10))
    
    return do_transfer_lite, ctx.args.user_accounts + 1, lambda: _yield_parameterizations(ctx)


def _yield_parameterizations(ctx: ExecutionContext) -> typing.Generator:
    """Yields parameterizations to be dispatched to actor via a message queue.
    
    """
    # Dapp contract account refund.
    yield (
        ctx,
        constants.ACC_RUN_CONTRACT,
        constants.ACC_RUN_FAUCET,
    )

    # Dapp user accounts refund.
    for account_index in range(constants.ACC_RUN_USERS, ctx.args.user_accounts + constants.ACC_RUN_USERS):
        yield (
            ctx,
            account_index,
            constants.ACC_RUN_FAUCET,
        )


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    pass
