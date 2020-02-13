import time

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.domain import AccountType
from stests.core.domain import RunContext
from stests.core.utils import factory



# Queue to which messages will be dispatched.
_QUEUE = f"global.accounts"


@dramatiq.actor(queue_name=_QUEUE)
def do_create_account(ctx: RunContext, index: int, typeof: AccountType):
    """Creates an account for use during the course of the simulation.
    
    """
    # Instantiate.
    account = factory.create_account(index=index, typeof=typeof)

    # Cache.
    cache.set_account(ctx, account)

    # Chain.
    return ctx


@dramatiq.actor(queue_name=_QUEUE)
def do_transfer_clx(
    ctx: RunContext,
    cp1_account_type: AccountType, 
    cp1_account_index: int,
    cp2_account_type: AccountType, 
    cp2_account_index: int,
    motes: int
    ):
    """Performs a CLX transfer between 2 counterparties.
    
    """
    # Set node.
    node = cache.get_ctx_node(ctx)

    # Set counterparties.
    cp1 = cache.get_account(ctx, cp1_account_type, cp1_account_index)
    cp2 = cache.get_account(ctx, cp2_account_type, cp2_account_index)

    # Transfer CLX from node -> faucet.
    deploy = clx.do_transfer(node, cp1, cp2, motes)

    # Update cache.
    cache.set_deploy(ctx, deploy)

    # Temporary until properly hooking into streams.
    time.sleep(4.0)

    # Chain.
    return ctx


@dramatiq.actor(queue_name=_QUEUE)
def do_transfer_clx_and_verify(
    ctx: RunContext,
    cp1_account_type: AccountType, 
    cp1_account_index: int,
    cp2_account_type: AccountType, 
    cp2_account_index: int,
    motes: int
    ):
    """Performs a CLX transfer between 2 counterparties & verifies transfers.

    """
    # Set node.
    node = cache.get_ctx_node(ctx)

    # Set counterparties.
    cp1 = cache.get_account(ctx, cp1_account_type, cp1_account_index)
    cp2 = cache.get_account(ctx, cp2_account_type, cp2_account_index)

    # Set balances.
    cp1_balance = clx.get_balance(node, cp1)
    cp2_balance = clx.get_balance(node, cp2)

    # Transfer CLX from node -> faucet.
    deploy = clx.do_transfer(node, cp1, cp2, motes)

    # Update cache.
    cache.set_deploy(ctx, deploy)

    # Temporary until properly hooking into streams.
    time.sleep(4.0)

    # Assert balances.
    assert clx.get_balance(node, cp1) <= cp1_balance - motes
    assert clx.get_balance(node, cp2) == cp2_balance + motes

    # Chain.
    return ctx
