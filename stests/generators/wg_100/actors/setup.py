import time

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.domain import AccountType
from stests.core.domain import RunContext
from stests.core.domain import NetworkIdentifier
from stests.core.domain import NodeIdentifier
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
def do_fund_faucet(ctx: RunContext):
    """Funds account to be used as a faucet.
    
    """
    # Set node.
    # TODO: randomize if node index = 0.
    node = cache.get_node(ctx.node_id)

    # Set faucet account.
    faucet = cache.get_account(ctx, AccountType.FAUCET, 1)

    # Transfer CLX from node -> faucet.
    deploy = clx.do_transfer(node, node.account, faucet, 100000000)

    # Update cache.
    cache.set_deploy(ctx, deploy)

    # Temporary until properly hooking into streams.
    time.sleep(3.0)

    # Chain.
    return ctx


@dramatiq.actor(queue_name=_QUEUE)
def do_fund_contract(ctx: RunContext):
    """Funds contract account (from faucet).
    
    """
    # Set node.
    # TODO: randomize if node index = 0.
    node = cache.get_node(ctx.node_id)

    # Set faucet account.
    faucet = cache.get_account(ctx, AccountType.FAUCET, 1)

    # Set contract account.
    contract = cache.get_account(ctx, AccountType.CONTRACT, 1)

    # Transfer CLX from node -> faucet.
    deploy = clx.do_transfer(node, faucet, contract, 10000000)

    # Update cache.
    cache.set_deploy(ctx, deploy)

    # Temporary until properly hooking into streams.
    time.sleep(3.0)

    # Chain.
    return ctx


@dramatiq.actor(queue_name=_QUEUE)
def do_fund_user(ctx: RunContext, account_index: int):
    """Funds user account (from faucet).
    
    """
    # Set node.
    # TODO: randomize if node index = 0.
    node = cache.get_node(ctx.node_id)

    # Set faucet account.
    faucet = cache.get_account(ctx, AccountType.FAUCET, 1)

    # Set user account.
    user = cache.get_account(ctx, AccountType.USER, account_index)

    # Transfer CLX from node -> faucet.
    deploy = clx.do_transfer(node, faucet, user, 10000000)

    # Update cache.
    cache.set_deploy(ctx, deploy)

    # Temporary until properly hooking into streams.
    time.sleep(3.0)

    # Chain.
    return ctx


@dramatiq.actor(queue_name=_QUEUE)
def do_deploy_contract(ctx: RunContext):
    """Deploys smart contract to target network.
    
    """
    print("TODO: do_deploy_contract :: 1. pull account.  2. Dispatch deploy.  3. Monitor deploy.")
    binary_fpath = resources.get_wasm_path(constants.WASM_CONTRACT_FILENAME)
    print(binary_fpath)
    return ctx

    # clx.do_deploy_contract(ctx, account, binary_fpath)