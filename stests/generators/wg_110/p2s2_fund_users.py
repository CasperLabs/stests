import typing
import dramatiq

from stests import chain
from stests.core.types.chain import DeployType
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.core.utils.exceptions import IgnoreableAssertionError
from stests.generators.utils import accounts
from stests.generators.utils import constants
from stests.generators.utils import verification


# Step label.
LABEL = "fund-users"


def execute(ctx: ExecutionContext) -> typing.Union[dramatiq.Actor, int, typing.Callable]:
    """Step entry point.
    
    :param ctx: Execution context information.

    :returns: 3 member tuple -> actor, message count, message arg factory.

    """
    def _yield_parameterizations() -> typing.Generator:
        for deploy_idx in range(1, ctx.args.transfers + 1):  
            yield (
                ctx,
                accounts.get_account_idx_for_run_faucet(ctx.args.accounts, ctx.args.transfers),
                accounts.get_account_idx_for_deploy(ctx.args.accounts, deploy_idx),
                ctx.args.amount + chain.DEFAULT_TX_FEE_NATIVE_TRANSFER,
                DeployType.TRANSFER_WASM,
            )

    return accounts.do_transfer, ctx.args.transfers, _yield_parameterizations


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    verification.verify_deploy_count(ctx, ctx.args.transfers)


def verify_deploy(ctx: ExecutionContext, node_id: NodeIdentifier, block_hash: str, deploy_hash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param node_id: Identifier of node emitting chain event.
    :param block_hash: Hash of block in which deploy was batched.
    :param deploy_hash: Hash of deploy being processed.

    """
    verification.verify_deploy(ctx, block_hash, deploy_hash)


def verify_deploy_batch_is_complete(ctx: ExecutionContext, deploy_index: int):
    """Step deploy batch is complete verifier.
    
    :param ctx: Execution context information.
    :param deploy_index: Index of a finalized deploy in relation to deploys dispatched during this step.

    """
    assert deploy_index == ctx.args.transfers
