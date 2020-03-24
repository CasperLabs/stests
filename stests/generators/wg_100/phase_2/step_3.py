from stests.core.orchestration import ExecutionContext
from stests.generators import utils
from stests.generators.wg_100 import constants



# Step description.
DESCRIPTION = "Refunds funds previously transferred to a run-faucet account."

# Step label.
LABEL = "refund-faucet"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """     
    utils.do_refund.send(
        ctx,
        constants.ACC_RUN_FAUCET,
        constants.ACC_NETWORK_FAUCET,
        False
    )


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    utils.verify_deploy_count(ctx, 1)


def verify_deploy(ctx: ExecutionContext, bhash: str, dhash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param dhash: A deploy hash.

    """
    utils.verify_deploy(ctx, bhash, dhash)
    utils.verify_transfer(ctx, dhash)
