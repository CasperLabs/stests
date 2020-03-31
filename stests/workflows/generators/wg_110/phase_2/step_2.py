import random
import typing

from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.workflows.generators.utils import verification
from stests.workflows.generators.utils.accounts import do_refund
from stests.workflows.generators.wg_100 import constants



# Step description.
DESCRIPTION = "Refunds funds previously transferred to user accounts."

# Step label.
LABEL = "refund-users"


def execute(ctx: ExecutionContext) -> typing.Callable:
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    # Set dispatch window.
    deploy_count = ctx.args.user_accounts
    dispatch_window = ctx.get_dispatch_window_ms(deploy_count)

    # Refund: user -> run faucet.
    for acc_index in range(constants.ACC_RUN_USERS, ctx.args.user_accounts + constants.ACC_RUN_USERS):
        do_refund.send_with_options(
            args = (
                ctx,
                acc_index,
                constants.ACC_RUN_FAUCET,
                True
            ),
            delay=random.randint(0, dispatch_window)
        )    


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    verification.verify_deploy_count(ctx, ctx.args.user_accounts) 


def verify_deploy(ctx: ExecutionContext, node_id: NodeIdentifier, bhash: str, dhash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param dhash: A deploy hash.

    """
    verification.verify_deploy(ctx, bhash, dhash)
    verification.verify_transfer(ctx, bhash, dhash)
