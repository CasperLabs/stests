import typing

import dramatiq

from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.workflows.generators.utils import constants
from stests.workflows.generators.utils import verification
from stests.workflows.generators.utils.accounts import do_fund_account



# Step label.
LABEL = "fund-contract"


def execute(ctx: ExecutionContext) -> typing.Union[dramatiq.Actor, tuple]:
    """Step entry point.
    
    :param ctx: Execution context information.

    :returns: 2 member tuple -> actor, args.

    """
    return do_fund_account, (
        ctx,
        constants.ACC_RUN_FAUCET,
        constants.ACC_RUN_CONTRACT,
        ctx.args.contract_initial_clx_balance,
    )


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    verification.verify_deploy_count(ctx, 1)    


def verify_deploy(ctx: ExecutionContext, node_id: NodeIdentifier, block_hash: str, deploy_hash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param node_id: Identifier of node that emitted finalization event.
    :param block_hash: Hash of a finalized block.
    :param deploy_hash: Hash of a finalized deploy.

    """
    verification.verify_deploy(ctx, block_hash, deploy_hash)
    verification.verify_transfer(ctx, node_id, block_hash, deploy_hash)
