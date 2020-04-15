import typing

from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.workflows.generators.utils import verification
from stests.workflows.generators.utils.accounts import do_fund_account
from stests.workflows.generators.wg_210 import constants



# Step label.
LABEL = "fund-users"


def execute(ctx: ExecutionContext) -> typing.Callable:
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    def get_messages():
        for acc_index in range(constants.ACC_RUN_USERS, ctx.args.user_accounts + constants.ACC_RUN_USERS):
            yield do_fund_account.message(
                ctx,
                constants.ACC_RUN_FAUCET,
                acc_index,
                ctx.args.user_initial_clx_balance,
                True
            )

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
    transfer = verification.verify_transfer(ctx, bhash, dhash)
    verification.verify_account_balance(ctx, node_id, bhash, transfer.cp2_index, ctx.args.user_initial_clx_balance)
