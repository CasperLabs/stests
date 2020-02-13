import time

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.cache.identifiers import NetworkIdentifier
from stests.core.cache.identifiers import NodeIdentifier
from stests.core.domain import Account
from stests.core.domain import AccountType
from stests.core.domain import Node
from stests.core.domain import RunContext
from stests.core.utils import factory
from stests.core.utils import resources
from stests.generators.wg_100 import constants



# Queue to which message will be dispatched.
_QUEUE = f"{constants.TYPE}.setup"


@dramatiq.actor(queue_name=_QUEUE)
def do_flush_cache(ctx: RunContext):   
    """Flushes cache in preparation for a new run.
    
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
    node = cache.get_ctx_node(ctx)

    # Set counterparties.
    cp1 = node.account
    cp2 = cache.get_account(ctx, AccountType.FAUCET, 1)

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


@dramatiq.actor(queue_name=_QUEUE)
def do_deploy_contract(ctx: RunContext):
    """Deploys smart contract to target network.
    
    """
    print("TODO: do_deploy_contract :: 1. pull account.  2. Dispatch deploy.  3. Monitor deploy.")
    binary_fpath = resources.get_wasm_path(constants.WASM_CONTRACT_FILENAME)
    print(binary_fpath)

    # Chain.
    return ctx
