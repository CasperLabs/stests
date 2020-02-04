import dramatiq

from stests.core.types import AccountType
from stests.generators.wg_100 import metadata
from stests.generators.wg_100.phase_01.actors.auction import do_start_auction
from stests.generators.wg_100.phase_01.actors.setup import do_create_account
from stests.generators.wg_100.phase_01.actors.setup import do_deploy_contract
from stests.generators.wg_100.phase_01.actors.setup import do_flush_cache
from stests.generators.wg_100.phase_01.actors.setup import do_fund_contract
from stests.generators.wg_100.phase_01.actors.setup import do_fund_faucet
from stests.generators.wg_100.phase_01.actors.setup import do_fund_user


# Queue to which message will be dispatched.
_QUEUE = f"{metadata.TYPE}.phase_01.orchestrator"


# TODO: chunk user account creating/funding ?


def execute(ctx):
    """Orchestrates execution of WG-100 workflow.
    
    """
    do_flush_cache.send_with_options(
        args=(ctx, ), 
        on_success=on_flush_cache
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_flush_cache(_, ctx):
    do_create_account.send_with_options(
        args=(ctx, 1, AccountType.FAUCET),
        on_success=on_create_faucet_account
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_create_faucet_account(_, ctx):
    do_create_account.send_with_options(
        args=(ctx, 1, AccountType.CONTRACT),
        on_success=on_create_contract_account
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_create_contract_account(_, ctx):
    def get_message(index):
        return do_create_account.message(ctx, index, AccountType.USER)

    def get_messages():
        return list(map(get_message, range(1, ctx.args.user_accounts + 1)))

    g = dramatiq.group(get_messages())
    g.add_completion_callback(on_create_user_accounts.message(ctx))
    g.run()


@dramatiq.actor(queue_name=_QUEUE)
def on_create_user_accounts(ctx):
    do_fund_faucet.send_with_options(
        args=(ctx, ), on_success=on_fund_faucet
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_fund_faucet(_, ctx):
    do_fund_contract.send_with_options(
        args=(ctx, ), on_success=on_fund_contract
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_fund_contract(_, ctx):
    def get_message(idx):
        return do_fund_user.message(ctx, idx)

    def get_messages():
        return list(map(get_message, range(1, ctx.args.user_accounts + 1)))

    g = dramatiq.group(get_messages())
    g.add_completion_callback(on_fund_users.message(ctx))
    g.run()


@dramatiq.actor(queue_name=_QUEUE)
def on_fund_users(ctx):
    do_deploy_contract.send_with_options(
        args=(ctx, ), on_success=on_deploy_contract
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_deploy_contract(_, ctx):
    do_start_auction.send_with_options(
        args=(ctx, ), on_success=on_start_auction
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_start_auction(_, ctx):
    print("TIME TO GO HOME")

