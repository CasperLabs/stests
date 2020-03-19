import typing

from stests.core.domain import AccountType
from stests.core.domain import ClientContractType
from stests.core.orchestration import ExecutionContext
from stests.core.utils import logger
from stests.generators import utils
from stests.generators.wg_200 import constants



# Step description.
DESCRIPTION = "Dispatches a notification to signal that generator has completed."

# Step label.
LABEL = "set-user-contract-hashes"


def execute(ctx: ExecutionContext) -> typing.Callable:
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    def get_messages():
        for acc_index in range(constants.ACC_RUN_USERS, ctx.args.user_accounts + constants.ACC_RUN_USERS):
            yield utils.do_set_contract.message(ctx, acc_index, ClientContractType.COUNTER_DEFINE)

    return get_messages


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    utils.verify_deploy_count(ctx, ctx.args.user_accounts)    


def verify_deploy(ctx: ExecutionContext, dhash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param dhash: A deploy hash.

    """
    utils.verify_deploy(ctx, dhash)
