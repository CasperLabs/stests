import typing

from stests.core.domain import RunContext
from stests.generators.wg_100 import constants
from stests.generators.wg_100.phase_1 import utils



# Step description.
DESCRIPTION = "Fund's a set of run user accounts."

# Step label.
LABEL = "fund-users"


def execute(ctx: RunContext) -> typing.Callable:
    """Step entry point.
    
    :param ctx: Generator run contextual information.

    """
    def get_messages():
        for acc_index in range(constants.ACC_RUN_USERS, ctx.args.user_accounts + constants.ACC_RUN_USERS):
            yield utils.do_fund_account.message(
                ctx,
                constants.ACC_RUN_FAUCET,
                acc_index,
                ctx.args.user_initial_clx_balance
            )

    return get_messages


def verify_deploy(ctx: RunContext, dhash: str):
    """Step deploy verifier.
    
    :param ctx: Generator run contextual information.
    :param dhash: A deploy hash.

    """
    utils.verify_deploy(ctx, dhash)
    transfer = utils.verify_transfer(ctx, dhash)
    utils.verify_account_balance(ctx, transfer.cp2_index, ctx.args.user_initial_clx_balance)
    utils.verify_deploy_count(ctx, ctx.args.user_accounts)    
