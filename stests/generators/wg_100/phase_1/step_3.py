from stests.core.orchestration import ExecutionContext
from stests.generators.wg_100 import constants
from stests.generators.wg_100 import utils_verification as uv
from stests.generators.wg_100.phase_1 import utils



# Step description.
DESCRIPTION = "Fund's a run contract account."

# Step label.
LABEL = "fund-contract"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    utils.do_fund_account.send(
        ctx,
        constants.ACC_RUN_FAUCET,
        constants.ACC_RUN_CONTRACT,
        ctx.args.contract_initial_clx_balance
        )


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    uv.verify_deploy_count(ctx, 1)    


def verify_deploy(ctx: ExecutionContext, dhash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param dhash: A deploy hash.

    """
    uv.verify_deploy(ctx, dhash)
    transfer = uv.verify_transfer(ctx, dhash)
    uv.verify_account_balance(ctx, transfer.cp2_index, ctx.args.contract_initial_clx_balance)
