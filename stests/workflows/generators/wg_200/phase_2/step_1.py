import typing

from stests.core.domain import AccountType
from stests.core.domain import ContractType
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.core.utils import logger
from stests.workflows.generators.utils import verification
from stests.workflows.generators.utils.contracts import do_set_contract
from stests.workflows.generators.wg_200 import constants



# Step description.
DESCRIPTION = "Dispatches a notification to signal that generator has completed."

# Step label.
LABEL = "counter-define-wasm"


def execute(ctx: ExecutionContext) -> typing.Callable:
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    # raise NotImplementedError("TODO: apply rate limiting")

    def get_messages():
        for account_index in range(constants.ACC_RUN_USERS, ctx.args.user_accounts + constants.ACC_RUN_USERS):
            yield do_set_contract.message(ctx, account_index, ContractType.COUNTER_DEFINE)

    return get_messages


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
