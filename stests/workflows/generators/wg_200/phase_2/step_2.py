import random
import typing

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.domain import DeployType
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.core.utils import factory
from stests.workflows.generators.utils import verification
from stests.workflows.generators.wg_200 import constants



# Step description.
DESCRIPTION = "Dispatches a notification to signal that generator has completed."

# Step label.
LABEL = "counter-call"


def execute(ctx: ExecutionContext) -> typing.Callable:
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    # Set dispatch window.
    deploy_count = ctx.args.user_accounts
    deploy_dispatch_window = ctx.get_dispatch_window_ms(deploy_count)

    # Increment counter of contract instance deployed under users account.
    for account_index in range(constants.ACC_RUN_USERS, ctx.args.user_accounts + constants.ACC_RUN_USERS):
        for _ in range(0, ctx.args.increments):
            _increment_counter_0.send_with_options(
                args = (ctx, account_index),
                delay=random.randint(0, deploy_dispatch_window)
            )


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    verification.verify_deploy_count(ctx, ctx.args.user_accounts * ctx.args.increments)    


def verify_deploy(ctx: ExecutionContext, node_id: NodeIdentifier, block_hash: str, deploy_hash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param node_id: Identifier of node which emitted block finalisation event.
    :param block_hash: A finalized block hash.
    :param deploy_hash: A finalized deploy hash.

    """
    deploy = verification.verify_deploy(ctx, block_hash, deploy_hash)
    account = cache.state.get_account_by_index(ctx, deploy.account_index)
    count = clx.contracts.counter_define.get_count(node_id, account, block_hash)
    assert count == ctx.args.increments, "counter verification failed"


@dramatiq.actor(queue_name=constants.QUEUE)
def _increment_counter_0(ctx: ExecutionContext, account_index: int):
    """Dispatches counter increment deploy.
    
    """
    # Set account.
    account = cache.state.get_account_by_index(ctx, account_index)

    # Increment on-chain.
    (node, deploy_hash) = clx.contracts.counter_define.increment(ctx, account)

    # Set info. 
    deploy = factory.create_deploy_for_run(
        account=account,
        ctx=ctx, 
        node=node, 
        deploy_hash=deploy_hash, 
        typeof=DeployType.COUNTER_DEFINE
        )

    # Update cache.
    cache.state.set_deploy(deploy)
