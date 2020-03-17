import typing

from stests.core.domain import AccountType
from stests.core.orchestration import ExecutionContext
from stests.generators import utils
from stests.generators.wg_110 import constants


# Step description.
DESCRIPTION = "Creates run accounts"

# Step label.
LABEL = "create-accounts"


def execute(ctx: ExecutionContext) -> typing.Callable:
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    def get_messages():
        yield utils.do_create_account.message(ctx, constants.ACC_RUN_FAUCET, AccountType.FAUCET)
        yield utils.do_create_account.message(ctx, constants.ACC_RUN_CONTRACT, AccountType.CONTRACT)
        for index in range(constants.ACC_RUN_USERS, ctx.args.user_accounts + constants.ACC_RUN_USERS):
            yield utils.do_create_account.message(ctx, index, AccountType.USER)

    return get_messages


def verify(ctx):
    """Step execution verifier.
    
    :param ctx: Execution context information.

    """    
    # TODO: get count of created accounts and confirm = ctx.args.user_accounts + 2
    return True
