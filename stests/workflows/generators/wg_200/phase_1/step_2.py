from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.workflows.generators.utils import verification
from stests.workflows.generators.utils.accounts import do_fund_account
from stests.workflows.generators.wg_200 import constants



# Step label.
LABEL = "fund-run-faucet"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    do_fund_account.send(
        ctx,
        constants.ACC_NETWORK_FAUCET,
        constants.ACC_RUN_FAUCET,
        ctx.args.faucet_initial_clx_balance,
        True
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
    verification.verify_account_balance(ctx, node_id, bhash, transfer.cp2_index, ctx.args.faucet_initial_clx_balance)
