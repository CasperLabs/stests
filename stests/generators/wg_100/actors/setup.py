import time

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.domain import Account
from stests.core.domain import AccountType
from stests.core.domain import NetworkIdentifier
from stests.core.domain import Node
from stests.core.domain import NodeIdentifier
from stests.core.domain import RunContext
from stests.core.utils import factory
from stests.core.utils import resources
from stests.generators.wg_100 import constants



# Queue to which message will be dispatched.
_QUEUE = f"{constants.TYPE}.phase_01.setup"


@dramatiq.actor(queue_name=_QUEUE)
def do_reset_cache(ctx: RunContext):   
    """Resets cache in preparation for a new run.
    
    """
    # Flush previous cache data.
    cache.flush_run(ctx)

    # Cache.
    cache.set_run_context(ctx)

    # Chain.
    return ctx


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
def do_fund_faucet(ctx: RunContext, motes: int):
    """Funds account to be used as a faucet.
    
    """
    # Set node.
    # TODO: randomize if node index = 0.
    node = cache.get_node(ctx.node_id)

    # Set counterparties.
    cp1 = node.account
    cp2 = cache.get_account(ctx, AccountType.FAUCET, 1)

    # Transfer CLX.
    _do_transfer(ctx, node, cp1, cp2, motes)

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
    # TODO: randomize if node index = 0.
    node = cache.get_node(ctx.node_id)

    # Set counterparties.
    cp1 = cache.get_account(ctx, cp1_account_type, cp1_account_index)
    cp2 = cache.get_account(ctx, cp2_account_type, cp2_account_index)

    # Transfer CLX.
    _do_transfer(ctx, node, cp1, cp2, motes)

    # Chain.
    return ctx


def _do_transfer(ctx, node: Node, cp1: Account, cp2: Account, motes):
    """Transfers CLX between accounts.
    
    """
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


@dramatiq.actor(queue_name=_QUEUE)
def do_deploy_contract(ctx: RunContext):
    """Deploys smart contract to target network.
    
    """
    print("TODO: do_deploy_contract :: 1. pull account.  2. Dispatch deploy.  3. Monitor deploy.")
    binary_fpath = resources.get_wasm_path(constants.WASM_CONTRACT_FILENAME)
    print(binary_fpath)
    return ctx

    # clx.do_deploy_contract(ctx, account, binary_fpath)