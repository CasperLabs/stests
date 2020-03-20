import dramatiq

from stests.core import cache
from stests.core.domain import AccountType
from stests.core.orchestration import ExecutionContext
from stests.core.utils import factory



# Queue to which messages will be dispatched.
_QUEUE = "orchestration.utils"


@dramatiq.actor(queue_name=_QUEUE)
def do_create_account(ctx: ExecutionContext, index: int, typeof: AccountType):
    """Creates an account for use during the course of a simulation.

    :param ctx: Execution context information.
    :param index: Run specific account index.
    :param typeof: Account type.

    """
    account = factory.create_account_for_run(ctx, index=index, typeof=typeof)
    cache.state.set_account(account)
