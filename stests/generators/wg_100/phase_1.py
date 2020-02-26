import typing

from stests.core import cache
from stests.core import clx
from stests.core.domain import AccountType
from stests.core.domain import RunContext
from stests.core.mq.actor import actorify
from stests.core.utils import factory
from stests.generators.wg_100.constants import *



@actorify(on_success=lambda: do_create_accounts)
def do_init_cache(ctx: RunContext):   
    """Initiliases cache in preparation for a new run.
    
    :param ctx: Generator run contextual information.

    """
    cache.set_run_context(ctx)


@actorify(on_success=lambda: do_fund_faucet)
def do_create_accounts(ctx: RunContext) -> typing.Callable:
    """Creates run specific accounts.
    
    :param ctx: Generator run contextual information.

    """
    def get_messages():
        yield do_create_account.message(ctx, ACC_RUN_FAUCET, AccountType.FAUCET)
        yield do_create_account.message(ctx, ACC_RUN_CONTRACT, AccountType.CONTRACT)
        for index in range(ACC_RUN_USERS, ctx.args.user_accounts + ACC_RUN_USERS):
            yield do_create_account.message(ctx, index, AccountType.USER)

    return get_messages


@actorify()
def do_fund_faucet(ctx: RunContext):
    """Funds account to be used as a faucet.
    
    :param ctx: Generator run contextual information.

    """
    do_fund_account.send(
        ctx,
        ACC_NETWORK_FAUCET,
        ACC_RUN_FAUCET,
        ctx.args.faucet_initial_clx_balance
        )


@actorify()
def do_fund_contract(ctx: RunContext):
    """Funds account to be used as a contract.
    
    :param ctx: Generator run contextual information.

    """
    do_fund_account.send(
        ctx,
        ACC_RUN_FAUCET,
        ACC_RUN_CONTRACT,
        ctx.args.contract_initial_clx_balance
        )


@actorify()
def do_fund_users(ctx) -> typing.Callable:
    """Funds accounts to be used as users.
    
    :param ctx: Generator run contextual information.

    """    
    def get_messages():
        for acc_index in range(ACC_RUN_USERS, ctx.args.user_accounts + ACC_RUN_USERS):
            yield do_fund_account.message(
                ctx,
                ACC_RUN_FAUCET,
                acc_index,
                ctx.args.user_initial_clx_balance
            )

    return get_messages


@actorify(is_substep=True)
def do_create_account(ctx: RunContext, index: int, typeof: AccountType):
    """Creates an account for use during the course of a simulation.

    :param ctx: Generator run contextual information.
    :param index: Run specific account index.
    :param typeof: Account type.

    """
    account = factory.create_account_for_run(ctx, index=index, typeof=typeof)
    cache.set_run_account(account)


@actorify(is_substep=True)
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
        cp1 = cache.get_run_account(ctx, cp1_index)
    cp2 = cache.get_run_account(ctx, cp2_index)

    # Transfer CLX from cp1 -> cp2.
    (deploy, transfer) = clx.do_transfer(ctx, cp1, cp2, motes)

    # Update cache.
    cache.set_run_deploy(deploy)
    cache.set_run_transfer(transfer)
