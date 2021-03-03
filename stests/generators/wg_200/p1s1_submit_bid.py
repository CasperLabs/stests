from stests import chain
from stests.core import cache
from stests.core import factory
from stests.core.types.chain import DeployType
from stests.core.types.orchestration import ExecutionContext
from stests.generators.utils.infra import get_network_node



# Step label.
LABEL = "auction-bid-submit"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    # Set validator.
    _, validator = get_network_node(ctx, ctx.args.validator_index)
    
    # Set target network / node.
    network, node = get_network_node(ctx)

    # Submit deploy.
    print(node)
    dispatch_info = chain.DeployDispatchInfo(validator.account, network, node)
    print(dispatch_info)
        
    deploy_hash, dispatch_duration, dispatch_attempts = \
        chain.set_auction_bid_submit(
            dispatch_info,
            ctx.args.amount,
            ctx.args.delegation_rate
            )

    # Update cache: deploy.
    cache.state.set_deploy(factory.create_deploy_for_run(
        ctx=ctx, 
        account=validator.account,
        node=node, 
        deploy_hash=deploy_hash, 
        dispatch_attempts=dispatch_attempts,
        dispatch_duration=dispatch_duration,
        typeof=DeployType.AUCTION_BID_SUBMIT
        ))  
