import typing

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.domain import ContractType
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.workflows.generators.utils import constants
from stests.workflows.generators.utils import verification



# Step label.
LABEL = "invoke-wasm"


def execute(ctx: ExecutionContext) -> typing.Union[dramatiq.Actor, int, typing.Callable]:
    """Step entry point.
    
    :param ctx: Execution context information.

    :returns: 3 member tuple -> actor, message count, message arg factory.

    """
    # Set account.
    account = cache.state.get_account_by_index(ctx, constants.ACC_RUN_CONTRACT)

    # Query account's named keys.

    print(account)    


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    print(222)
