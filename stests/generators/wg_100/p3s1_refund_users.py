import typing
import dramatiq

from stests.core.types.chain import DeployType
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.core.utils.exceptions import IgnoreableAssertionError
from stests.generators.utils import accounts
from stests.generators.utils import constants
from stests.generators.utils import verification


# Step label.
LABEL = "refund-users"


def execute(ctx: ExecutionContext) -> typing.Union[dramatiq.Actor, int, typing.Callable]:
    """Step entry point.
    
    :param ctx: Execution context information.

    :returns: 2 member tuple -> actor, message args.

    """
    def _yield_parameterizations() -> typing.Generator:
        for deploy_idx in range(1, ctx.args.transfers + 1):  
            yield (
                ctx,
                accounts.get_account_idx_for_deploy(ctx.args.accounts, deploy_idx),
                accounts.get_account_idx_for_run_faucet(ctx.args.accounts, ctx.args.transfers),
                DeployType.TRANSFER_NATIVE,
            )

    return accounts.do_refund, ctx.args.transfers, _yield_parameterizations


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    verification.verify_deploy_count(ctx, len(accounts.get_account_range(ctx.args.accounts, ctx.args.transfers)))


def verify_deploy(ctx: ExecutionContext, node_id: NodeIdentifier, block_hash: str, deploy_hash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param node_id: Identifier of node emitting chain event.
    :param block_hash: Hash of block in which deploy was batched.
    :param deploy_hash: Hash of deploy being processed.
    :param deploy_index: Index of a finalized deploy in relation to the deploys dispatched during this step.

    """
    verification.verify_deploy(ctx, block_hash, deploy_hash)


def verify_deploy_batch_is_complete(ctx: ExecutionContext, deploy_index: int):
    """Step deploy batch is complete verifier.
    
    :param ctx: Execution context information.
    :param deploy_index: Index of a finalized deploy in relation to the deploys dispatched during this step.

    """
    assert deploy_index == len(accounts.get_account_range(ctx.args.accounts, ctx.args.transfers))
