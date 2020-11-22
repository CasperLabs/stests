from stests import chain
from stests.core import cache
from stests.core import factory
from stests.core.types.chain import AccountType
from stests.core.types.chain import DeployType
from stests.core.types.orchestration import ExecutionContext
from stests.generators.utils import verification
from stests.generators.utils.infra import get_network_node



# Step label.
LABEL = "auction-bid-submit"

# Account index of user dispatching bid submission.
_USER_ACCOUNT_INDEX = 1


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    # Set target network / node.
    network, node = get_network_node(ctx)

    # Set validator account.
    validator = factory.create_account_for_run(ctx, AccountType.USER, _USER_ACCOUNT_INDEX)

    # Submit deploy.
    dispatch_info = chain.DeployDispatchInfo(validator, network, node)
    deploy_hash, dispatch_duration, dispatch_attempts = \
        chain.set_auction_bid_submit(
            dispatch_info,
            ctx.args.amount,
            ctx.args.delegation_rate
            )

    # Update cache: deploy.
    cache.state.set_deploy(factory.create_deploy_for_run(
        ctx=ctx, 
        account=validator,
        node=node, 
        deploy_hash=deploy_hash, 
        dispatch_attempts=dispatch_attempts,
        dispatch_duration=dispatch_duration,
        typeof=DeployType.AUCTION_BID_SUBMIT
        ))  


def verify(ctx: ExecutionContext):
    """Step execution verifier.
    
    :param ctx: Execution context information.

    """
    verification.verify_deploy_count(ctx, 1) 
