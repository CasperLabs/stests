import dramatiq

from stests.core.domain import AccountType
from stests.generators.wg_100 import constants
from stests.generators.wg_100.actors.auction import do_start_auction
from stests.generators.wg_100.actors.setup import do_create_account
from stests.generators.wg_100.actors.setup import do_deploy_contract
from stests.generators.wg_100.actors.setup import do_fund_faucet
from stests.generators.wg_100.actors.setup import do_reset_cache
from stests.generators.wg_100.actors.setup import do_transfer_clx


# Queue to which message will be dispatched.
_QUEUE = f"{constants.TYPE}.phase_01.orchestrator"


# TODO: chunk user account creating/funding ?


def execute(ctx):
    """Orchestrates execution of WG-100 workflow.

    :param ctx: Contextual information passed along flow of execution.
    
    """
    do_reset_cache.send_with_options(
        args=(ctx, ), 
        on_success=on_reset_cache
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_reset_cache(_, ctx):
    """Callback: on_flush_cache.
    
    """
    do_create_account.send_with_options(
        args=(ctx, 1, AccountType.FAUCET),
        on_success=on_create_faucet_account
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_create_faucet_account(_, ctx):
    """Callback: on_create_faucet_account.
    
    """
    do_create_account.send_with_options(
        args=(ctx, 1, AccountType.CONTRACT),
        on_success=on_create_contract_account
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_create_contract_account(_, ctx):
    """Callback: on_create_contract_account.
    
    """
    def get_messages():
        for index in range(1, ctx.args.user_accounts + 1):
            yield do_create_account.message(ctx, index, AccountType.USER)

    g = dramatiq.group(get_messages())
    g.add_completion_callback(on_create_user_accounts.message(ctx))
    g.run()


@dramatiq.actor(queue_name=_QUEUE)
def on_create_user_accounts(ctx):
    """Callback: on_create_user_accounts.
    
    """
    do_fund_faucet.send_with_options(
        args=(ctx, ),
        on_success=on_fund_faucet
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_fund_faucet(_, ctx):
    """Callback: on_fund_faucet.
    
    """
    do_transfer_clx.send_with_options(
        args=(
            ctx,
            AccountType.FAUCET, 1,
            AccountType.CONTRACT, 1,
            ctx.args.contract_initial_clx_balance
            ),
        on_success=on_fund_contract
    )


@dramatiq.actor(queue_name=_QUEUE)
def on_fund_contract(_, ctx):
    """Callback: on_fund_contract.
    
    """
    def get_messages():
        for index in range(1, ctx.args.user_accounts + 1):
            yield do_transfer_clx.message(
                ctx,
                AccountType.FAUCET, 1,
                AccountType.USER, index,
                ctx.args.user_initial_clx_balance
            )

    g = dramatiq.group(get_messages())
    g.add_completion_callback(on_fund_users.message(ctx))
    g.run()


@dramatiq.actor(queue_name=_QUEUE)
def on_fund_users(ctx):
    """Callback: on_fund_users.
    
    """
    do_deploy_contract.send_with_options(
        args=(ctx, ),
        on_success=on_deploy_contract
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_deploy_contract(_, ctx):
    """Callback: on_deploy_contract.
    
    """
    do_start_auction.send_with_options(
        args=(ctx, ),
        on_success=on_start_auction
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_start_auction(_, ctx):
    """Callback: on_start_auction.
    
    """
    print("TIME TO GO HOME")
