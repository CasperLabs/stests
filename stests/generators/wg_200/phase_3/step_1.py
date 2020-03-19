import typing

from stests.core.orchestration import ExecutionContext
from stests.generators import utils
from stests.generators.wg_200 import constants



# Step description.
DESCRIPTION = "Refunds funds previously transferred from run faucet."

# Step label.
LABEL = "refund-run-faucet"


def execute(ctx: ExecutionContext) -> typing.Callable:
    """Step entry point.
    
    :param ctx: Execution context information.

    """  
    def get_messages():
        for acc_index in range(constants.ACC_RUN_USERS, ctx.args.user_accounts + constants.ACC_RUN_USERS):
            yield utils.do_refund.message(
                ctx,
                acc_index,
                constants.ACC_RUN_FAUCET,
                True
            )

    return get_messages


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    utils.verify_deploy_count(ctx, ctx.args.user_accounts) 


def verify_deploy(ctx: ExecutionContext, dhash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param dhash: A deploy hash.

    """
    utils.verify_deploy(ctx, dhash)
    utils.verify_refund(ctx, dhash)