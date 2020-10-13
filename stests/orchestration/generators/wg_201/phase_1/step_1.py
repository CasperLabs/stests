from stests.core.types.orchestration import ExecutionContext
from stests.orchestration.generators.utils import verification
from stests.orchestration.generators.utils import auction



# Step label.
LABEL = "auction-bid-withdraw"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    auction.do_bid_withdraw(ctx, 1, ctx.args.amount)


def verify(ctx: ExecutionContext):
    """Step execution verifier.
    
    :param ctx: Execution context information.

    """
    verification.verify_deploy_count(ctx, 1) 


# TODO: when event stream is hooked up then: 1. Listen to events;  2. Asynchronously correlate run deploy.  3. Continue next phase of workflow.
