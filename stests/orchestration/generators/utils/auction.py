import typing

import dramatiq

from stests import chain
from stests.core import cache
from stests.core import factory
from stests.core.types.chain import Account
from stests.core.types.chain import ContractType
from stests.core.types.chain import DeployType
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.types.orchestration import ExecutionAspect
from stests.core.types.orchestration import ExecutionContext

from stests.orchestration.generators.utils.accounts import get_account


# Queue to which messages will be dispatched.
_QUEUE = "orchestration.generators.auction"


@dramatiq.actor(queue_name=_QUEUE)
def do_submit_bid(
    ctx: ExecutionContext,
    account_index: int,
    amount: int,
    delegation_rate: int,
    ):
    """Executes a wasm-vased account token transfer between counter-parties.

    :param ctx: Execution context information.
    :param account_index: Account index of bidder.
    :param bid_amount: Bid amount (in motes).
    :param delegation_rate: Delegation rate paid out to delegators.
    
    """
    # Set target network / node.
    network_id = factory.create_network_id(ctx.network)
    network = cache.infra.get_network(network_id)
    node = cache.infra.get_node_by_network(network)

    validator = get_account(ctx, network, 0)

    deploy_hash, dispatch_duration, dispatch_attempts = chain.set_auction_bid_submit(
        network,
        node,
        validator,
        amount=amount,
        delegation_rate=delegation_rate,
    )

    # Update cache: deploy.
    cache.state.set_deploy(factory.create_deploy_for_run(
        ctx=ctx, 
        account=validator,
        node=node, 
        deploy_hash=deploy_hash, 
        dispatch_attempts=dispatch_attempts,
        dispatch_duration=dispatch_duration,
        typeof=DeployType.AUCTION_BID
        ))
    
    # Increment deploy counts.
    # Note: this is temporary until we can increment during deploy finalisation.
    cache.orchestration.increment_deploy_count(ctx, ExecutionAspect.RUN)
    cache.orchestration.increment_deploy_count(ctx, ExecutionAspect.PHASE)
    cache.orchestration.increment_deploy_count(ctx, ExecutionAspect.STEP)
