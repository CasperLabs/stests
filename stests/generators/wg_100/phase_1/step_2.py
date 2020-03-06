import typing

from stests.core.domain import AccountType
from stests.core.domain import RunContext
from stests.generators.wg_100 import constants
from stests.generators.wg_100.phase_1 import utils


# Step description.
DESCRIPTION = "Creates run accounts"

# Step label.
LABEL = "create-accounts"


def execute(ctx: RunContext) -> typing.Callable:
    """Step entry point.
    
    :param ctx: Generator run contextual information.

    """
    def get_messages():
        yield utils.do_create_account.message(ctx, constants.ACC_RUN_FAUCET, AccountType.FAUCET)
        yield utils.do_create_account.message(ctx, constants.ACC_RUN_CONTRACT, AccountType.CONTRACT)
        for index in range(ACC_RUN_USERS, ctx.args.user_accounts + constants.ACC_RUN_USERS):
            yield utils.do_create_account.message(ctx, index, AccountType.USER)

    return get_messages


def verify(ctx):
    """Step execution verifier.
    
    :param ctx: Generator run contextual information.

    """    
    return True
