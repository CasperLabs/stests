from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.generators import utils
from stests.generators.wg_210 import constants



# Step description.
DESCRIPTION = "Fund's a run faucet account."

# Step label.
LABEL = "fund-faucet"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    utils.do_fund_account.send(
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
    utils.verify_deploy_count(ctx, 1)  
    

def verify_deploy(ctx: ExecutionContext, node_id: NodeIdentifier, bhash: str, dhash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param dhash: A deploy hash.

    """
    utils.verify_deploy(ctx, bhash, dhash)
    transfer = utils.verify_transfer(ctx, bhash, dhash)
    utils.verify_account_balance(ctx, bhash, transfer.cp2_index, ctx.args.faucet_initial_clx_balance)
