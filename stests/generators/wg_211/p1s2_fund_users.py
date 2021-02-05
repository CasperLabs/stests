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
LABEL = "fund-users"


def execute(ctx: ExecutionContext) -> typing.Union[dramatiq.Actor, int, typing.Callable]:
    """Step entry point.
    
    :param ctx: Execution context information.

    :returns: 3 member tuple -> actor, message count, message arg factory.

    """
    def _yield_parameterizations() -> typing.Generator:
        for account_index in range(1, ctx.args.delegators + 1):
            yield (
                ctx,
                accounts.get_account_idx_for_network_faucet(),
                account_index,
                ctx.args.amount_to_fund,
                DeployType.TRANSFER_NATIVE,
            )

    return accounts.do_transfer, ctx.args.delegators, _yield_parameterizations


def verify(ctx: ExecutionContext):
    """Step verifier.
    
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
    verification.verify_account_balance_on_transfer(
        ctx,
        node_id,
        deploy.state_root_hash,
        deploy.associated_account_index,
        ctx.args.amount_to_fund,
        )


def verify_deploy_batch_is_complete(ctx: ExecutionContext, deploy_index: int):
    """Step deploy batch is complete verifier.
    
    :param ctx: Execution context information.
    :param deploy_index: Index of a finalized deploy in relation to deploys dispatched during this step.

    """
    assert deploy_index == ctx.args.delegators
