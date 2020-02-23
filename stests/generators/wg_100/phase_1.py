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
_QUEUE = f"generators.{constants.TYPE.lower()}"


@dramatiq.actor(queue_name=_QUEUE)
def do_fund_faucet(ctx: RunContext, account_index: int, motes: int):
    """Funds account to be used as a faucet.
    
    :param ctx: Generator run contextual information.
    :param account_index: Run specific index of account acting as run faucet.
    :param motes: Amount to be transferred.

    """
    # Set network.
    network = cache.get_run_network(ctx)
    if not network.faucet:
        raise ValueError("Network faucet account does not exist.")

    # Set counterparties.
    cp1 = network.faucet
    cp2 = cache.get_run_account(ctx, account_index)

    # Transfer CLX from network faucet -> run faucet.
    (deploy, transfer) = clx.do_transfer(ctx, cp1, cp2, motes)

    # Update cache.
    cache.set_run_deploy(deploy)
    cache.set_run_transfer(transfer)

    # Chain.
    return ctx


@dramatiq.actor(queue_name=_QUEUE)
def do_deploy_contract(ctx: RunContext):
    """Deploys smart contract to target network.
    
    :param ctx: Generator run contextual information.

    """
    print("TODO: do_deploy_contract :: 1. pull account.  2. Dispatch deploy.  3. Monitor deploy.")
    binary_fpath = resources.get_wasm_path(constants.WASM_CONTRACT_FILENAME)
    print(binary_fpath)

    # Chain.
    return ctx


@dramatiq.actor(queue_name=_QUEUE)
def do_start_auction(ctx):
    """Initialise auction phase.
    
    :param ctx: Generator run contextual information.

    """
    print("TODO: do_start_auction :: 1. Establish transfer sequence.")

    # Chain.
    return ctx
