import random
import typing

from stests.core.domain import AccountType
from stests.core.domain import ContractType
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.core.utils import logger
from stests.workflows.generators.utils import verification
from stests.workflows.generators.utils.contracts import do_set_contract
from stests.workflows.generators.wg_200 import constants



# Step label.
LABEL = "counter-define-wasm"


def execute(ctx: ExecutionContext) -> typing.Callable:
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    # Set dispatch window.
    deploy_count = ctx.args.user_accounts
    deploy_dispatch_window = ctx.get_dispatch_window_ms(deploy_count)

    # Insdtall contract under each user account.
    for account_index in range(constants.ACC_RUN_USERS, ctx.args.user_accounts + constants.ACC_RUN_USERS):
        do_set_contract.send_with_options(
            args = (ctx, account_index, ContractType.COUNTER_DEFINE),
            delay=random.randint(0, deploy_dispatch_window)
        )


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    verification.verify_deploy_count(ctx, ctx.args.user_accounts)    


def verify_deploy(ctx: ExecutionContext, node_id: NodeIdentifier, bhash: str, dhash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param dhash: A deploy hash.

    """
    verification.verify_deploy(ctx, bhash, dhash)
