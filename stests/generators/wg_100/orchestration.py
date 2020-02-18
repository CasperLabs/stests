import dramatiq

from stests.core.domain import AccountType
from stests.core.domain import RunContext

from stests.core.actors.account import do_create_account
from stests.core.actors.account import do_fund_account_and_verify
from stests.core.actors.misc import do_cache_context
from stests.core.actors.misc import do_flush_cache

from stests.generators.wg_100 import constants
from stests.generators.wg_100.phase_1 import do_start_auction
from stests.generators.wg_100.phase_1 import do_deploy_contract
from stests.generators.wg_100.phase_1 import do_fund_faucet


# Queue to which message will be dispatched.
_QUEUE = f"generators.{constants.TYPE.lower()}"

# Account index: faucet.
ACC_INDEX_FAUCET = 1

# Account index: contract.
ACC_INDEX_CONTRACT = 2

# Account index: users.
ACC_INDEX_USERS = 3



def execute(ctx: RunContext):
    """Orchestrates execution of WG-100 workflow.

    :param ctx: Contextual information passed along flow of execution.
    
    """
    # TODO: chunk user account creating/funding ?
    do_flush_cache.send_with_options(
        args=(ctx, ), 
        on_success=on_flush_cache
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_flush_cache(_, ctx: RunContext):
    """Callback: on_flush_cache.
    
    """
    do_cache_context.send_with_options(
        args=(ctx, ), 
        on_success=on_cache_context
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_cache_context(_, ctx: RunContext):
    """Callback: on_cache_context.
    
    """
    do_create_account.send_with_options(
        args=(ctx, ACC_INDEX_FAUCET, AccountType.FAUCET),
        on_success=on_create_faucet_account
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_create_faucet_account(_, ctx: RunContext):
    """Callback: on_create_faucet_account.
    
    """
    do_create_account.send_with_options(
        args=(ctx, ACC_INDEX_CONTRACT, AccountType.CONTRACT),
        on_success=on_create_contract_account
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_create_contract_account(_, ctx: RunContext):
    """Callback: on_create_contract_account.
    
    """
    def get_messages():
        for index in range(ACC_INDEX_USERS, ctx.args.user_accounts + ACC_INDEX_USERS):
            yield do_create_account.message(ctx, index, AccountType.USER)

    g = dramatiq.group(get_messages())
    g.add_completion_callback(on_create_user_accounts.message(ctx))
    g.run()


@dramatiq.actor(queue_name=_QUEUE)
def on_create_user_accounts(ctx: RunContext):
    """Callback: on_create_user_accounts.
    
    """
    do_fund_faucet.send_with_options(
        args=(ctx, ACC_INDEX_FAUCET, ctx.args.faucet_initial_clx_balance),
        on_success=on_fund_faucet
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_fund_faucet(_, ctx: RunContext):
    """Callback: on_fund_faucet.
    
    """
    do_fund_account_and_verify.send_with_options(
        args=(ctx, ACC_INDEX_FAUCET, ACC_INDEX_CONTRACT, ctx.args.contract_initial_clx_balance),
        on_success=on_fund_contract
    )


@dramatiq.actor(queue_name=_QUEUE)
def on_fund_contract(_, ctx: RunContext):
    """Callback: on_fund_contract.
    
    """
    def get_messages():
        for index in range(ACC_INDEX_USERS, ctx.args.user_accounts + ACC_INDEX_USERS):
            yield do_fund_account_and_verify.message(
                ctx, ACC_INDEX_FAUCET, index, ctx.args.user_initial_clx_balance
            )

    g = dramatiq.group(get_messages())
    g.add_completion_callback(on_fund_users.message(ctx))
    g.run()


@dramatiq.actor(queue_name=_QUEUE)
def on_fund_users(ctx: RunContext):
    """Callback: on_fund_users.
    
    """
    do_deploy_contract.send_with_options(
        args=(ctx, ),
        on_success=on_deploy_contract
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_deploy_contract(_, ctx: RunContext):
    """Callback: on_deploy_contract.
    
    """
    do_start_auction.send_with_options(
        args=(ctx, ),
        on_success=on_start_auction
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_start_auction(_, ctx: RunContext):
    """Callback: on_start_auction.
    
    """
    print("TIME TO GO HOME")
