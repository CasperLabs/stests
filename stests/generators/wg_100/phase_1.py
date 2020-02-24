import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.actors.account import do_create_account
from stests.core.actors.account import do_fund_account
from stests.core.domain import AccountType
from stests.core.domain import RunContext
from stests.core.mq.actor import actorify
from stests.core.utils import factory
from stests.core.utils import resources
from stests.generators.wg_100 import constants
from stests.generators.wg_100 import phase_2



# Account index: faucet.
ACC_INDEX_FAUCET = 1

# Account index: contract.
ACC_INDEX_CONTRACT = 2

# Account index: users.
ACC_INDEX_USERS = 3


@actorify(on_success=lambda: do_create_accounts)
def do_init_cache(ctx: RunContext):   
    """Initiliases cache in preparation for a new run.
    
    :param ctx: Generator run contextual information.

    """
    # Persist context.
    cache.set_run_context(ctx)


@actorify(on_success=lambda: do_fund_faucet)
def do_create_accounts(ctx: RunContext) -> dramatiq.group:
    """Funds contract account.
    
    :param ctx: Generator run contextual information.

    """
    # Message factory.
    def get_messages():
        yield do_create_account.message(ctx, ACC_INDEX_FAUCET, AccountType.FAUCET)
        yield do_create_account.message(ctx, ACC_INDEX_CONTRACT, AccountType.CONTRACT)
        for index in range(ACC_INDEX_USERS, ctx.args.user_accounts + ACC_INDEX_USERS):
            yield do_create_account.message(ctx, index, AccountType.USER)

    return dramatiq.group(get_messages())


@actorify(on_success=lambda: do_fund_contract)
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


@actorify(on_success=lambda: do_fund_users)
def do_fund_contract(ctx: RunContext):
    """Funds contract account.
    
    :param ctx: Generator run contextual information.

    """
    # Fund account.
    do_fund_account.send(ctx, ACC_INDEX_FAUCET, ACC_INDEX_CONTRACT, ctx.args.contract_initial_clx_balance)


@actorify(on_success=lambda: do_deploy_contract)
def do_fund_users(ctx) -> dramatiq.group:
    """Funds user accounts.
    
    :param ctx: Generator run contextual information.

    """
    # Message factory.
    def get_messages():
        for index in range(ACC_INDEX_USERS, ctx.args.user_accounts + ACC_INDEX_USERS):
            yield do_fund_account.message(
                ctx, ACC_INDEX_FAUCET, index, ctx.args.user_initial_clx_balance
            )

    # Workflow group.
    return dramatiq.group(get_messages())


@actorify(on_success=lambda: phase_2.do_start_auction)
def do_deploy_contract(ctx: RunContext):
    """Deploys smart contract to target network.
    
    :param ctx: Generator run contextual information.

    """
    print("TODO: do_deploy_contract :: 1. pull account.  2. Dispatch deploy.  3. Monitor deploy.")
    binary_fpath = resources.get_wasm_path(constants.WASM_CONTRACT_FILENAME)
    print(binary_fpath)
