import time
import typing

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.actors.account import do_create_account
from stests.core.actors.account import do_fund_account
from stests.core.domain import Account
from stests.core.domain import AccountType
from stests.core.domain import NetworkIdentifier
from stests.core.domain import Node
from stests.core.domain import NodeIdentifier
from stests.core.domain import RunContext
from stests.core.utils import factory
from stests.core.utils import resources
from stests.generators.wg_100 import constants
from stests.generators.wg_100 import phase_2



# Queue to which message will be dispatched.
_QUEUE = f"generators.{constants.TYPE.lower()}"

# Account index: faucet.
ACC_INDEX_FAUCET = 1

# Account index: contract.
ACC_INDEX_CONTRACT = 2

# Account index: users.
ACC_INDEX_USERS = 3


@dramatiq.actor(queue_name=_QUEUE)
def do_init_cache(ctx: RunContext):   
    """Initiliases cache in preparation for a new run.
    
    :param ctx: Generator run contextual information.

    """
    # Persist step.
    cache.set_run_step(factory.create_run_step(ctx, "phase_1.do_reset_cache"))

    # Persist context.
    cache.set_run_context(ctx)

    # Chain.
    do_create_accounts.send(ctx)
    

@dramatiq.actor(queue_name=_QUEUE)
def do_create_accounts(ctx: RunContext):
    """Funds contract account.
    
    :param ctx: Generator run contextual information.

    """
    # Persist step.
    cache.set_run_step(factory.create_run_step(ctx, "phase_1.do_create_accounts"))

    # Message factory.
    def get_messages():
        yield do_create_account.message(ctx, ACC_INDEX_FAUCET, AccountType.FAUCET)
        yield do_create_account.message(ctx, ACC_INDEX_CONTRACT, AccountType.CONTRACT)
        for index in range(ACC_INDEX_USERS, ctx.args.user_accounts + ACC_INDEX_USERS):
            yield do_create_account.message(ctx, index, AccountType.USER)

    # Workflow group.
    g = dramatiq.group(get_messages())
    g.add_completion_callback(do_fund_faucet.message(ctx))
    g.run()


@dramatiq.actor(queue_name=_QUEUE)
def do_fund_faucet(ctx: RunContext):
    """Funds account to be used as a faucet.
    
    :param ctx: Generator run contextual information.

    """
    # Persist step.
    cache.set_run_step(factory.create_run_step(ctx, "phase_1.do_fund_faucet"))

    # Set network.
    network = cache.get_run_network(ctx)
    if not network.faucet:
        raise ValueError("Network faucet account does not exist.")

    # Set counterparties.
    cp1 = network.faucet
    cp2 = cache.get_run_account(ctx, ACC_INDEX_FAUCET)

    # Transfer CLX from network faucet -> run faucet.
    (deploy, transfer) = clx.do_transfer(ctx, cp1, cp2, ctx.args.faucet_initial_clx_balance)

    # Update cache.
    cache.set_run_deploy(deploy)
    cache.set_run_transfer(transfer)


@dramatiq.actor(queue_name=_QUEUE)
def do_fund_contract(ctx: RunContext):
    """Funds contract account.
    
    :param ctx: Generator run contextual information.

    """
    # Persist step.
    cache.set_run_step(factory.create_run_step(ctx, "phase_1.do_fund_contract"))

    # Fund account.
    do_fund_account.send(ctx, ACC_INDEX_FAUCET, ACC_INDEX_CONTRACT, ctx.args.contract_initial_clx_balance)


@dramatiq.actor(queue_name=_QUEUE)
def do_fund_users(ctx):
    """Funds user accounts.
    
    :param ctx: Generator run contextual information.

    """
    # Persist step.
    cache.set_run_step(factory.create_run_step(ctx, "phase_1.do_fund_users"))

    # Message factory.
    def get_messages():
        for index in range(ACC_INDEX_USERS, ctx.args.user_accounts + ACC_INDEX_USERS):
            yield do_fund_account.message(
                ctx, ACC_INDEX_FAUCET, index, ctx.args.user_initial_clx_balance
            )

    # Workflow group.
    g = dramatiq.group(get_messages())
    g.run()


@dramatiq.actor(queue_name=_QUEUE)
def do_deploy_contract(ctx: RunContext):
    """Deploys smart contract to target network.
    
    :param ctx: Generator run contextual information.

    """
    # Persist step.
    cache.set_run_step(factory.create_run_step(ctx, "phase_1.do_deploy_contract"))

    print("TODO: do_deploy_contract :: 1. pull account.  2. Dispatch deploy.  3. Monitor deploy.")
    binary_fpath = resources.get_wasm_path(constants.WASM_CONTRACT_FILENAME)
    print(binary_fpath)

    # Chain.
    phase_2.do_start_auction.send(ctx)
