import typing

from stests.core.orchestration import ExecutionContextInfo
from stests.generators.wg_100 import constants
from stests.generators.wg_100.phase_3 import utils



# Step description.
DESCRIPTION = "Refunds funds previously transferred from run faucet."

# Step label.
LABEL = "refund-run-faucet"


def execute(ctx: ExecutionContextInfo) -> typing.Callable:
    """Step entry point.
    
    :param ctx: Execution context information.

    """  
    def get_messages():
        yield utils.do_refund.message(
            ctx,
            constants.ACC_RUN_CONTRACT,
            constants.ACC_RUN_FAUCET
        )
        for acc_index in range(constants.ACC_RUN_USERS, ctx.args.user_accounts + constants.ACC_RUN_USERS):
            yield utils.do_refund.message(
                ctx,
                acc_index,
                constants.ACC_RUN_FAUCET
            )

    return get_messages



def verify_deploy(ctx: ExecutionContextInfo, dhash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param dhash: A deploy hash.

    """
    utils.verify_deploy(ctx, dhash)
    utils.verify_refund(ctx, dhash)
    utils.verify_deploy_count(ctx, 1 + ctx.args.user_accounts) 
