import typing

import dramatiq

from stests.core.domain import AccountType
from stests.core.orchestration import ExecutionContext
from stests.workflows.generators.utils.accounts import do_create_account
from stests.workflows.generators.wg_100 import constants


# Step label.
LABEL = "create-accounts"


def execute(ctx: ExecutionContext) -> typing.Union[dramatiq.Actor, int, typing.Callable]:
    """Step entry point.
    
    :param ctx: Execution context information.

    :returns: 3 member tuple -> actor, message count, message arg factory.

    """
    return do_create_account, ctx.args.user_accounts + 2, lambda: _yield_parameterizations(ctx)


def _yield_parameterizations(ctx: ExecutionContext) -> typing.Generator:
    """Yields parameterizations to be dispatched to actor via a message queue.
    
    """
    yield ctx, constants.ACC_RUN_FAUCET, AccountType.FAUCET
    yield ctx, constants.ACC_RUN_CONTRACT, AccountType.CONTRACT
    for index in range(constants.ACC_RUN_USERS, ctx.args.user_accounts + constants.ACC_RUN_USERS):
        yield ctx, index, AccountType.USER


def verify(ctx):
    """Step execution verifier.
    
    :param ctx: Execution context information.

    """    
    # TODO: get count of created accounts and confirm = ctx.args.user_accounts + 2
    return True
