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
from stests.orchestration.generators.utils.infra import get_network_node


# Queue to which messages will be dispatched.
_QUEUE = "orchestration.generators.auction"


@dramatiq.actor(queue_name=_QUEUE)
def do_bid_submit(
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
    network, node = get_network_node(ctx)

    # Set validator account.
    validator = get_account(ctx, network, 0)

    # Submit auction bid.
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
    # Note: this is temporary until incremented during deploy finalisation.
    cache.orchestration.increment_deploy_counts(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def do_bid_withdraw(
    ctx: ExecutionContext,
    account_index: int,
    amount: int,
    ):
    """Executes a wasm-vased account token transfer between counter-parties.

    :param ctx: Execution context information.
    :param account_index: Account index of bidder.
    :param bid_amount: Bid amount (in motes).
    
    """
    # Set target network / node.
    network, node = get_network_node(ctx)

    # Set validator account.
    validator = get_account(ctx, network, 0)

    # Withdraw auction bid.
    deploy_hash, dispatch_duration, dispatch_attempts = chain.set_auction_bid_withdraw(
        network,
        node,
        validator,
        amount=amount,
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
    # Note: this is temporary until incremented during deploy finalisation.
    cache.orchestration.increment_deploy_counts(ctx)
