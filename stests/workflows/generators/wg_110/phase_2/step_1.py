import typing

import dramatiq

from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.workflows.generators.utils import verification
from stests.workflows.generators.utils.accounts import do_refund
from stests.workflows.generators.wg_110 import constants



# Step label.
LABEL = "refund-contract"


def execute(ctx: ExecutionContext) -> typing.Union[dramatiq.Actor, tuple]:
    """Step entry point.
    
    :param ctx: Execution context information.

    :returns: 2 member tuple -> actor, args.

    """
    return do_refund, (
        ctx,
        constants.ACC_RUN_CONTRACT,
        constants.ACC_RUN_FAUCET,
    )


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    # Verify count of finialised deploys.
    verification.verify_deploy_count(ctx, 1) 


def verify_deploy(ctx: ExecutionContext, node_id: NodeIdentifier, block_hash: str, deploy_hash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param node_id: Identifier of node that emitted finalization event.
    :param block_hash: Hash of a finalized block.
    :param deploy_hash: Hash of a finalized deploy.

    """
    verification.verify_deploy(ctx, block_hash, deploy_hash)
    verification.verify_transfer(ctx, block_hash, deploy_hash)
