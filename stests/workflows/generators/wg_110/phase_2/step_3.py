from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.workflows.generators.utils import verification
from stests.workflows.generators.utils.accounts import do_refund
from stests.workflows.generators.wg_110 import constants



# Step label.
LABEL = "refund-run-faucet"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """     
    do_refund.send(
        ctx,
        constants.ACC_RUN_FAUCET,
        constants.ACC_NETWORK_FAUCET,
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
    verification.verify_transfer(ctx, bhash, dhash)
