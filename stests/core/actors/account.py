import time

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.domain import AccountType
from stests.core.domain import RunContext
from stests.core.utils import factory



# Queue to which messages will be dispatched.
_QUEUE = "generators.shared"


@dramatiq.actor(queue_name=_QUEUE)
def do_create_account(ctx: RunContext, index: int, typeof: AccountType):
    """Creates an account for use during the course of the simulation.

    :param ctx: Generator run contextual information.
    :param index: Run specific account index.
    :param typeof: Account type.

    """
    # Instantiate & encache.
    cache.set_run_account(ctx, factory.create_account(
        index=index,
        typeof=typeof
        ))

    # Chain.
    return ctx


@dramatiq.actor(queue_name=_QUEUE)
def do_fund_account_and_verify(ctx: RunContext, cp1_index: int, cp2_index: int, motes: int):
    """Performs a CLX transfer between 2 counterparties.

    :param ctx: Generator run contextual information.
    :param cp1_index: Run specific account index of counter-party one.
    :param cp2_index: Run specific account index of counter-party two.
    :param motes: Amount to be transferred.
    
    """
    # Set counterparties.
    cp1 = cache.get_run_account(ctx, cp1_index)
    cp2 = cache.get_run_account(ctx, cp2_index)

    # Set balances.
    cp1_balance = clx.get_balance(ctx, cp1)
    cp2_balance = clx.get_balance(ctx, cp2)

    # Transfer CLX from cp1 -> cp2.
    (deploy, transfer) = clx.do_transfer(ctx, cp1, cp2, motes)

    # Update cache.
    cache.set_run_deploy(ctx, deploy)
    cache.set_run_transfer(ctx, transfer)

    # Temporary until properly hooking into streams.
    time.sleep(4.0)

    # Assert balances.
    assert clx.get_balance(ctx, cp1) <= cp1_balance - motes
    assert clx.get_balance(ctx, cp2) == cp2_balance + motes

    # Chain.
    return ctx
