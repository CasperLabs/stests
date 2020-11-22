import typing
import dramatiq

from stests.core.types.chain import DeployType
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.generators.utils import constants
from stests.generators.utils import verification
from stests.generators.utils.accounts import do_transfer



# Step label.
LABEL = "do-transfers"


def execute(ctx: ExecutionContext) -> typing.Union[dramatiq.Actor, int, typing.Callable]:
    """Step entry point.
    
    :param ctx: Execution context information.

    :returns: 3 member tuple -> actor, message count, message arg factory.

    """
    def _yield_parameterizations() -> typing.Generator:
        for account_index in range(1, ctx.args.transfers + 1):
            yield (
                ctx,
                constants.ACC_NETWORK_FAUCET,
                account_index,
                ctx.args.amount,
                DeployType.TRANSFER_WASMLESS,
            )

    return do_transfer, ctx.args.transfers, _yield_parameterizations


def verify_deploy(ctx: ExecutionContext, node_id: NodeIdentifier, block_hash: str, deploy_hash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param node_id: Identifier of node that emitted finalization event.
    :param block_hash: Hash of a finalized block.
    :param deploy_hash: Hash of a finalized deploy.

    """
    verification.verify_deploy(ctx, block_hash, deploy_hash)
    # verification.verify_transfer(ctx, node_id, block_hash, deploy_hash)

