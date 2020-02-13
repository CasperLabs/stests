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
def do_fund_faucet(ctx: RunContext, account_index: int, motes: int):
    """Funds account to be used as a faucet.
    
    """
    # Set network.
    network = cache.get_network_by_ctx(ctx)
    if not network.faucet:
        raise ValueError("Network faucet account does not exist.")

    # Set counterparties.
    cp1 = network.faucet
    cp2 = cache.get_account_by_ctx(ctx, account_index)

    # Set balances.
    cp1_balance = clx.get_balance(ctx, cp1)
    cp2_balance = clx.get_balance(ctx, cp2)

    # Transfer CLX from network faucet -> run faucet.
    deploy = clx.do_transfer(ctx, cp1, cp2, motes)

    # Update cache.
    cache.set_deploy(ctx, deploy)

    # Temporary until properly hooking into streams.
    time.sleep(4.0)

    # Assert balances.
    assert clx.get_balance(ctx, cp1) <= cp1_balance - motes
    assert clx.get_balance(ctx, cp2) == cp2_balance + motes

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
