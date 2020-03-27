import typing

from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.generators import utils
from stests.generators.wg_100 import constants



# Step description.
DESCRIPTION = "Refunds funds previously transferred to a contract account."

# Step label.
LABEL = "refund-contract"


def execute(ctx: ExecutionContext) -> typing.Callable:
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    # Refund: contract -> run faucet.
    utils.do_refund.send(
        ctx,
        constants.ACC_RUN_CONTRACT,
        constants.ACC_RUN_FAUCET,
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
    utils.verify_transfer(ctx, bhash, dhash)
