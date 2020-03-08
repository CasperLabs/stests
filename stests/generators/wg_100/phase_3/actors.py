import typing

from stests.core import cache
from stests.core import clx
from stests.core.domain import Account
from stests.core.domain import AccountType
from stests.core.domain import ExecutionRunInfo
from stests.core.mq.actor import actorify
from stests.core.utils import factory
from stests.core.utils import logger
from stests.generators.wg_100.constants import *



@actorify()
def do_refund_step_1(ctx: ExecutionRunInfo) -> typing.Callable:
    """Refunds from user to run facuet.
    
    :param ctx: Generator run contextual information.

    """    
    def get_messages():
        yield do_refund.message(
            ctx,
            ACC_RUN_CONTRACT,
            ACC_RUN_FAUCET
        )
        for acc_index in range(ACC_RUN_USERS, ctx.args.user_accounts + ACC_RUN_USERS):
            yield do_refund.message(
                ctx,
                acc_index,
                ACC_RUN_FAUCET
            )

    return get_messages


@actorify()
def do_refund_step_2(ctx: ExecutionRunInfo):
    """Refunds from user to run facuet.
    
    :param ctx: Generator run contextual information.

    """    
    do_refund.send(
        ctx,
        ACC_RUN_FAUCET,
        ACC_NETWORK_FAUCET
    )


@actorify()
def do_notify_completion(ctx: ExecutionRunInfo):
    """Emits a run completion notification message.
    
    :param ctx: Generator run contextual information.

    """        
    # TODO: push notification.
    logger.log(f"ACTOR :: {ctx.run_type} :: R-{str(ctx.run_index).zfill(3)} has completed")


@actorify(is_substep=True)
def do_refund(ctx: ExecutionRunInfo, cp1_index: int, cp2_index: int):
    """Performs a refund ot funds between 2 counterparties.

    :param ctx: Generator run contextual information.
    :param cp1_index: Run specific account index of counter-party one.
    :param cp2_index: Run specific account index of counter-party two.
    
    """
    # Pull accounts.
    cp1 = cache.get_account_by_run(ctx, cp1_index)
    if cp2_index == ACC_NETWORK_FAUCET:
        network = cache.get_run_network(ctx)
        if not network.faucet:
            raise ValueError("Network faucet account does not exist.")
        cp2 = network.faucet
    else:
        cp2 = cache.get_account_by_run(ctx, cp2_index)

    # Refund CLX from cp1 -> cp2.
    (deploy, refund) = clx.do_refund(ctx, cp1, cp2)

    # Update cache.
    cache.set_run_deploy(deploy)
    cache.set_run_transfer(refund)
