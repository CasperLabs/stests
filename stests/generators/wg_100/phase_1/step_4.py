from stests.core.orchestration import ExecutionRunInfo
from stests.generators.wg_100 import constants
from stests.generators.wg_100.phase_1 import utils


# Step description.
DESCRIPTION = "Fund's a run contract account."

# Step label.
LABEL = "fund-contract"


def execute(ctx: ExecutionRunInfo):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    utils.do_fund_account.send(
        ctx,
        constants.ACC_RUN_FAUCET,
        constants.ACC_RUN_CONTRACT,
        ctx.args.contract_initial_clx_balance
        )


def verify_deploy(ctx: ExecutionRunInfo, dhash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param dhash: A deploy hash.

    """
    utils.verify_deploy(ctx, dhash)
    transfer = utils.verify_transfer(ctx, dhash)
    utils.verify_account_balance(ctx, transfer.cp2_index, ctx.args.contract_initial_clx_balance)
    utils.verify_deploy_count(ctx, 1)    
