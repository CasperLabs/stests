import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.domain import AccountType
from stests.core.domain import DeployStatus
from stests.core.domain import RunContext
from stests.core.domain import Transfer
from stests.core.domain import TransferStatus
from stests.core.mq.actor import actorify
from stests.core.utils import factory



# Account index: network faucet.
ACC_NETWORK_FAUCET = 0


# Queue to which messages will be dispatched.
_QUEUE = "wg-100.utils"


@dramatiq.actor(queue_name=_QUEUE)
def do_create_account(ctx: RunContext, index: int, typeof: AccountType):
    """Creates an account for use during the course of a simulation.

    :param ctx: Generator run contextual information.
    :param index: Run specific account index.
    :param typeof: Account type.

    """
    account = factory.create_account_for_run(ctx, index=index, typeof=typeof)
    cache.set_run_account(account)


@dramatiq.actor(queue_name=_QUEUE)
def do_fund_account(ctx: RunContext, cp1_index: int, cp2_index: int, motes: int):
    """Funds an account by transfering CLX transfer between 2 counterparties.

    :param ctx: Generator run contextual information.
    :param cp1_index: Run specific account index of counter-party one.
    :param cp2_index: Run specific account index of counter-party two.
    :param motes: Amount to be transferred.
    
    """
    # Set counterparties.
    if cp1_index == ACC_NETWORK_FAUCET:
        network = cache.get_run_network(ctx)
        if not network.faucet:
            raise ValueError("Network faucet account does not exist.")
        cp1 = network.faucet
    else:
        cp1 = cache.get_account_by_run(ctx, cp1_index)
    cp2 = cache.get_account_by_run(ctx, cp2_index)

    # Transfer CLX from cp1 -> cp2.
    (deploy, transfer) = clx.do_transfer(ctx, cp1, cp2, motes)

    # Update cache.
    cache.set_run_deploy(deploy)
    cache.set_run_transfer(transfer)



def verify_deploy(ctx: RunContext, dhash: str):
    """Verifies that a deploy is in a finalized state.
    
    """
    deploy = cache.get_run_deploy(dhash)
    assert deploy
    assert deploy.status == DeployStatus.FINALIZED


def verify_deploy_count(ctx: RunContext, expected: int):
    """Verifies that a step's count of finalized deploys tallies.
    
    """
    assert cache.get_step_deploy_count(ctx) == expected


def verify_transfer(ctx: RunContext, dhash: str) -> Transfer:
    """Verifies that a transfer between counter-parties completed.
    
    """
    transfer = cache.get_run_transfer(dhash)
    assert transfer
    assert transfer.status == TransferStatus.COMPLETE

    return transfer


def verify_account_balance(ctx: RunContext, account_index: int, expected: int):
    """Verifies that an account balance is as per expectation.
    
    """
    account = cache.get_account_by_run(ctx, account_index)
    assert account
    assert clx.get_balance(ctx, account) == expected
