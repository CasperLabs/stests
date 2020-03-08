from stests.core.orchestration import ExecutionRunInfo
from stests.generators.wg_100 import constants
from stests.generators.wg_100.phase_1 import utils


# Step description.
DESCRIPTION = "Fund's a run contract account."

# Step label.
LABEL = "fund-contract"


def execute(ctx: ExecutionRunInfo):
    """Step entry point.
    
    :param ctx: Generator run contextual information.

    """
    utils.do_fund_account.send(
        ctx,
        constants.ACC_RUN_FAUCET,
        constants.ACC_RUN_CONTRACT,
        ctx.args.contract_initial_clx_balance
        )


def verify_deploy(ctx: ExecutionRunInfo, dhash: str):
    """Step deploy verifier.
    
    :param ctx: Generator run contextual information.
    :param dhash: A deploy hash.

    """
    print(111)
    utils.verify_deploy(ctx, dhash)
    print(222)
    transfer = utils.verify_transfer(ctx, dhash)
    print(333)
    utils.verify_account_balance(ctx, transfer.cp2_index, ctx.args.contract_initial_clx_balance)
    print(444)
    utils.verify_deploy_count(ctx, 1)    
    print(555)
