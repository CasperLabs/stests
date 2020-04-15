from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.workflows.generators.utils import verification
from stests.workflows.generators.utils.accounts import do_fund_account
from stests.workflows.generators.wg_100 import constants



# Step label.
LABEL = "fund-contract"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    return do_fund_account, (
        ctx,
        constants.ACC_RUN_FAUCET,
        constants.ACC_RUN_CONTRACT,
        ctx.args.contract_initial_clx_balance,
        False,
    )


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    verification.verify_deploy_count(ctx, 1)    


def verify_deploy(ctx: ExecutionContext, node_id: NodeIdentifier, bhash: str, dhash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param dhash: A deploy hash.

    """
    verification.verify_deploy(ctx, bhash, dhash)
    transfer = verification.verify_transfer(ctx, bhash, dhash)
    verification.verify_account_balance(ctx, node_id, bhash, transfer.cp2_index, ctx.args.contract_initial_clx_balance)
