import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.orchestration import ExecutionContext
from stests.generators.utils import constants



# Queue to which messages will be dispatched.
_QUEUE = "orchestration.utils"


@dramatiq.actor(queue_name=_QUEUE)
def do_fund_account(ctx: ExecutionContext, cp1_index: int, cp2_index: int, motes: int):
    """Funds an account by transfering CLX transfer between 2 counterparties.

    :param ctx: Execution context information.
    :param cp1_index: Run specific account index of counter-party one.
    :param cp2_index: Run specific account index of counter-party two.
    :param motes: Amount to be transferred.
    
    """
    # Set counterparties.
    if cp1_index == constants.ACC_NETWORK_FAUCET:
        network = cache.orchestration.get_run_network(ctx)
        if not network.faucet:
            raise ValueError("Network faucet account does not exist.")
        cp1 = network.faucet
    else:
        cp1 = cache.state.get_account_by_run(ctx, cp1_index)
    cp2 = cache.state.get_account_by_run(ctx, cp2_index)

    # Transfer CLX from cp1 -> cp2.
    (deploy, transfer) = clx.do_transfer(ctx, cp1, cp2, motes)

    # Update cache.
    cache.state.set_run_deploy(deploy)
    cache.state.set_run_transfer(transfer)


@dramatiq.actor(queue_name=_QUEUE)
def do_refund(ctx: ExecutionContext, cp1_index: int, cp2_index: int):
    """Performs a refund ot funds between 2 counterparties.

    :param ctx: Execution context information.
    :param cp1_index: Run specific account index of counter-party one.
    :param cp2_index: Run specific account index of counter-party two.
    
    """
    # Pull accounts.
    cp1 = cache.state.get_account_by_run(ctx, cp1_index)
    if cp2_index == constants.ACC_NETWORK_FAUCET:
        network = cache.orchestration.get_run_network(ctx)
        if not network.faucet:
            raise ValueError("Network faucet account does not exist.")
        cp2 = network.faucet
    else:
        cp2 = cache.state.get_account_by_run(ctx, cp2_index)

    # Refund CLX from cp1 -> cp2.
    (deploy, refund) = clx.do_refund(ctx, cp1, cp2)

    # Update cache.
    cache.state.set_run_deploy(deploy)
    cache.state.set_run_transfer(refund)
