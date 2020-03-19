import typing

from stests.core import cache
from stests.core import clx
from stests.core.domain import AccountType
from stests.core.domain import ClientContractType
from stests.core.orchestration import ExecutionContext
from stests.core.utils import factory
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
    for account_index in range(constants.ACC_RUN_USERS, ctx.args.user_accounts + constants.ACC_RUN_USERS):
        _set_user_contract_hash(ctx, account_index)


def _set_user_contract_hash(ctx, account_index):
    """Stores the users contract hash.
    
    """
    deploys = cache.state.get_deploys_by_account(ctx, account_index)
    if not deploys:
        "TODO: raise error"
        return
    deploy = deploys[0]

    # Set account.
    account = cache.state.get_account_by_index(ctx, account_index)

    # Set contract hash.
    chash = clx.get_contract_hash(ctx, account, deploy.deploy_hash)

    # Set contract.
    contract = factory.create_account_contract(
        ctx=ctx,
        account=account,
        chash=chash,
        typeof=ClientContractType.COUNTER_DEFINE
    )

    # Cache contract.
    cache.state.set_account_contract(contract)


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    return True
