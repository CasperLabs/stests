from stests.core.domain import ExecutionRunInfo
from stests.generators.wg_100 import constants
from stests.generators.wg_100.phase_1 import utils



# Step description.
DESCRIPTION = "Fund's a run faucet account."

# Step label.
LABEL = "fund-faucet"



def execute(ctx: ExecutionRunInfo):
    """Step entry point.
    
    :param ctx: Generator run contextual information.

    """
    utils.do_fund_account.send(
        ctx,
        constants.ACC_NETWORK_FAUCET,
        constants.ACC_RUN_FAUCET,
        ctx.args.faucet_initial_clx_balance
        )


def verify_deploy(ctx: ExecutionRunInfo, dhash: str):
    """Step deploy verifier.
    
    :param ctx: Generator run contextual information.
    :param dhash: A deploy hash.

    """
    utils.verify_deploy(ctx, dhash)
    transfer = utils.verify_transfer(ctx, dhash)
    utils.verify_account_balance(ctx, transfer.cp2_index, ctx.args.faucet_initial_clx_balance)
    utils.verify_deploy_count(ctx, 1)
