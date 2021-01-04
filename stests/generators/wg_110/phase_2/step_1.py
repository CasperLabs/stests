import typing
import dramatiq

from stests.core.types.chain import DeployType
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.generators.utils import accounts
from stests.generators.utils import constants
from stests.generators.utils import verification



# Step label.
LABEL = "fund-run-faucet"


def execute(ctx: ExecutionContext) -> typing.Union[dramatiq.Actor, int, typing.Callable]:
    """Step entry point.
    
    :param ctx: Execution context information.

    :returns: 2 member tuple -> actor, message args.

    """
    return accounts.do_transfer, (
        ctx,
        constants.ACC_NETWORK_FAUCET,
        constants.ACC_RUN_FAUCET,
        ctx.args.faucet_initial_balance,
        DeployType.TRANSFER_WASM,
    )


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    verification.verify_deploy_count(ctx, 1)


def verify_deploy(ctx: ExecutionContext, node_id: NodeIdentifier, block_hash: str, deploy_hash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param node_id: Identifier of node emitting chain event.
    :param block_hash: Hash of block in which deploy was batched.
    :param deploy_hash: Hash of deploy being processed.

    """
    deploy = verification.verify_deploy(ctx, block_hash, deploy_hash)

    verification.verify_account_balance_on_transfer(
        ctx,
        node_id,
        deploy.state_root_hash,
        constants.ACC_RUN_FAUCET,
        ctx.args.faucet_initial_balance,
        )    


def verify_deploy_batch_is_complete(ctx: ExecutionContext, deploy_index: int):
    """Step deploy batch is complete verifier.
    
    :param ctx: Execution context information.
    :param deploy_index: Index of a finalized deploy in relation to deploys dispatched during this step.

    """
    assert deploy_index == 1
