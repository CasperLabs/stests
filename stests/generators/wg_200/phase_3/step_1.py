import typing

from stests.core.orchestration import ExecutionContext
from stests.generators import utils
from stests.generators.wg_200 import constants



# Step description.
DESCRIPTION = "Refunds funds previously transferred from run faucet."

# Step label.
LABEL = "refund-run-faucet"


def execute(ctx: ExecutionContext) -> typing.Callable:
    """Step entry point.
    
    :param ctx: Execution context information.

    """  
    print("TODO: invoke counter increment")


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    return True

