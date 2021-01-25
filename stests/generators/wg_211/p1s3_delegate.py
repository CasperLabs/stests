import typing

from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.generators.utils import verification
from stests.generators.utils import auction


# Step label.
LABEL = "auction-delegate"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    def _yield_parameterizations() -> typing.Generator:
        for account_index in range(1, ctx.args.delegators + 1):
            yield (
                ctx,
                account_index,
                ctx.args.amount,
            )

    return auction.do_delegate, ctx.args.delegators, _yield_parameterizations


def verify(ctx: ExecutionContext):
    """Step execution verifier.
    
    :param ctx: Execution context information.

    """
    verification.verify_deploy_count(ctx, ctx.args.delegators) 


def verify_deploy(ctx: ExecutionContext, node_id: NodeIdentifier, block_hash: str, deploy_hash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param node_id: Identifier of node emitting chain event.
    :param block_hash: Hash of block in which deploy was batched.
    :param deploy_hash: Hash of deploy being processed.
    :param deploy_index: Index of a finalized deploy in relation to the deploys dispatched during this step.

    """
    deploy = verification.verify_deploy(ctx, block_hash, deploy_hash)


def verify_deploy_batch_is_complete(ctx: ExecutionContext, deploy_index: int):
    """Step deploy batch is complete verifier.
    
    :param ctx: Execution context information.
    :param deploy_index: Index of a finalized deploy in relation to deploys dispatched during this step.

    """
    assert deploy_index == ctx.args.delegators
