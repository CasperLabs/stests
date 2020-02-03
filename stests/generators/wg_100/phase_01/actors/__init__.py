import dramatiq

from stests.generators.wg_100 import metadata
from stests.generators.wg_100.phase_01.actors.accounts import do_create_contract_account
from stests.generators.wg_100.phase_01.actors.accounts import do_create_faucet_account
from stests.generators.wg_100.phase_01.actors.accounts import do_create_user_account
from stests.generators.wg_100.phase_01.actors.accounts import do_fund_contract
from stests.generators.wg_100.phase_01.actors.accounts import do_fund_faucet
from stests.generators.wg_100.phase_01.actors.accounts import do_fund_user
from stests.generators.wg_100.phase_01.actors.contract import do_deploy_contract
from stests.generators.wg_100.phase_01.actors.setup import do_reset_cache



# Queue to which message will be dispatched.
_QUEUE = f"{metadata.TYPE}.phase_01.orchestrator"


def execute(ctx):
    """Orchestrates execution of WG-100 workflow.
    
    """
    do_reset_cache.send_with_options(
        args=(ctx, ),
        on_success=on_cache_reset
    )


@dramatiq.actor(queue_name=_QUEUE)
def on_cache_reset(_, ctx):
    # TODO: chunk user account creation as this may cause memory issue
    g = dramatiq.group([
            do_create_faucet_account.message(ctx),
            do_create_contract_account.message(ctx),
        ] + list(map(lambda idx: do_create_user_account.message(ctx, idx), range(1, ctx.user_accounts + 1))))
    g.add_completion_callback(on_accounts_created.message(ctx))
    g.run()


@dramatiq.actor(queue_name=_QUEUE)
def on_accounts_created(ctx):
    do_fund_faucet.send_with_options(
        args=(ctx, ),
        on_success=on_faucet_funded
    )


@dramatiq.actor(queue_name=_QUEUE)
def on_faucet_funded(_, ctx):
    do_fund_contract.send_with_options(
        args=(ctx, ),
        on_success=on_contract_funded
    )


@dramatiq.actor(queue_name=_QUEUE)
def on_contract_funded(_, ctx):
    # TODO: chunk user account funding ?
    g = dramatiq.group(
        list(map(lambda idx: do_fund_user.message(ctx, idx), range(1, ctx.user_accounts + 1)))
        )
    g.add_completion_callback(on_users_funded.message(ctx))
    g.run()


@dramatiq.actor(queue_name=_QUEUE)
def on_users_funded(ctx):
    do_deploy_contract.send_with_options(
        args=(ctx, ),
        on_success=on_contract_deployed
    )


@dramatiq.actor(queue_name=_QUEUE)
def on_contract_deployed(_, ctx):
    print("TIME TO GO HOME")
    print(ctx)

