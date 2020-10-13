import dramatiq

from stests import chain
from stests.chain.utils import DeployDispatchInfo
from stests.core import cache
from stests.core import factory
from stests.core.types.chain import DeployType
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
    """Submits a deploy bidding upon network's validator slot auction contract.

    :param ctx: Execution context information.
    :param account_index: Account index of bidder.
    :param bid_amount: Bid amount (in motes).
    :param delegation_rate: Delegation rate paid out to delegators.
    
    """
    # Set target network / node.
    network, node = get_network_node(ctx)

    # Set validator account.
    validator = get_account(ctx, network, 0)

    # Submit deploy.
    dispatch_info = DeployDispatchInfo(validator, network, node)
    deploy_hash, dispatch_duration, dispatch_attempts = \
        chain.set_auction_bid_submit(dispatch_info, amount, delegation_rate)

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
    
    # Update cache: deploy counts.
    # Note: this is temporary until incremented during deploy finalisation.
    cache.orchestration.increment_deploy_counts(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def do_bid_withdraw(
    ctx: ExecutionContext,
    account_index: int,
    amount: int,
    ):
    """Submits a deploy withdrawing a bid from network's validator slot auction contract.

    :param ctx: Execution context information.
    :param account_index: Account index of bidder.
    :param bid_amount: Bid amount (in motes).
    
    """
    # Set target network / node.
    network, node = get_network_node(ctx)

    # Set validator account.
    validator = get_account(ctx, network, 0)

    # Submit deploy.
    dispatch_info = DeployDispatchInfo(validator, network, node)
    deploy_hash, dispatch_duration, dispatch_attempts = \
        chain.set_auction_bid_withdraw(dispatch_info, amount)

    # Update cache: deploy.
    cache.state.set_deploy(factory.create_deploy_for_run(
        ctx=ctx, 
        account=validator,
        node=node, 
        deploy_hash=deploy_hash, 
        dispatch_attempts=dispatch_attempts,
        dispatch_duration=dispatch_duration,
        typeof=DeployType.AUCTION_BID_WITHDRAW
        ))
    
    # Update cache: deploy counts.
    # Note: this is temporary until incremented during deploy finalisation.
    cache.orchestration.increment_deploy_counts(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def do_delegate(ctx: ExecutionContext, account_index: int, amount: int):
    """Submits a deploy delegating an amount of tokens (in motes) to a validator for staking purposes.

    :param ctx: Execution context information.
    :param account_index: Account index of user delegating to the validator.
    :param bid_amount: Delegate amount (in motes).
    
    """
    _do_delegate_action(ctx, account_index, amount, DeployType.AUCTION_DELEGATE)


@dramatiq.actor(queue_name=_QUEUE)
def do_undelegate(ctx: ExecutionContext, account_index: int, amount: int):
    """Submits a deploy withdrawing a delegated amount of tokens (in motes) to a validator for staking purposes.

    :param ctx: Execution context information.
    :param account_index: Account index of bidder.
    :param bid_amount: Withdrawal amount (in motes).
    
    """
    _do_delegate_action(ctx, account_index, amount, DeployType.AUCTION_UNDELEGATE)


# Map: deploy type to associated deploy function.
DEPLOY_TYPE_TO_FN = {
    DeployType.AUCTION_DELEGATE: chain.set_auction_delegate,
    DeployType.AUCTION_UNDELEGATE: chain.set_auction_undelegate,
}


def _do_delegate_action(ctx: ExecutionContext, account_index: int, amount: int, deploy_type: DeployType.AUCTION_UNDELEGATE):
    # Set target network / node.
    network, node = get_network_node(ctx)

    # Set validator account.
    user = get_account(ctx, network, account_index)
    validator = node.account

    # Withdraw auction bid.
    dispatch_fn = DEPLOY_TYPE_TO_FN[deploy_type]
    dispatch_info = DeployDispatchInfo(validator, network, node)
    deploy_hash, dispatch_duration, dispatch_attempts = dispatch_fn(dispatch_info, validator, amount)

    # Update cache: deploy.
    cache.state.set_deploy(factory.create_deploy_for_run(
        ctx=ctx, 
        account=validator,
        node=node, 
        deploy_hash=deploy_hash, 
        dispatch_attempts=dispatch_attempts,
        dispatch_duration=dispatch_duration,
        typeof=DeployType.AUCTION_UNDELEGATE
        ))
    
    # Update cache: deploy counts.
    # Note: this is temporary until incremented during deploy finalisation.
    cache.orchestration.increment_deploy_counts(ctx)
