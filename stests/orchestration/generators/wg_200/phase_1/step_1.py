import typing

from stests.core import cache
from stests.core import factory
from stests.core.types.chain import AccountType
from stests.core.types.orchestration import ExecutionContext
from stests.orchestration.generators.utils import constants
from stests.orchestration.generators.utils import verification
from stests.orchestration.generators.utils.auction import do_submit_bid



# Step label.
LABEL = "auction-bid"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    do_submit_bid(ctx, 1, ctx.args.amount, ctx.args.delegation_rate)


def verify(ctx: ExecutionContext):
    """Step execution verifier.
    
    :param ctx: Execution context information.

    """
    verification.verify_deploy_count(ctx, 1) 
