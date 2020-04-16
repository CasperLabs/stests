import typing

import dramatiq

from stests.core.domain import ContractType
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.workflows.generators.utils import constants
from stests.workflows.generators.utils import verification
from stests.workflows.generators.utils.contracts import do_install_contract



# Step label.
LABEL = "install-wasm"


def execute(ctx: ExecutionContext) -> typing.Union[dramatiq.Actor, int, typing.Callable]:
    """Step entry point.
    
    :param ctx: Execution context information.

    :returns: 3 member tuple -> actor, message count, message arg factory.

    """
    return do_install_contract, (
        ctx,
        constants.ACC_RUN_CONTRACT,
        ContractType.COUNTER_DEFINE,
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
