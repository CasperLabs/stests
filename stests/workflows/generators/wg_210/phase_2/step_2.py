import typing

import dramatiq
from casperlabs_client.abi import ABI

from stests.core import cache
from stests.core import clx
from stests.core.domain import AccountType
from stests.core.domain import ContractType
from stests.core.domain import DeployType
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.core.utils import factory
from stests.core.utils import logger
from stests.workflows.generators.utils import verification
from stests.workflows.generators.wg_200 import constants



# Step label.
LABEL = "invoke-increment"


def execute(ctx: ExecutionContext) -> typing.Union[dramatiq.Actor, int, typing.Callable]:
    """Step entry point.
    
    :param ctx: Execution context information.

    :returns: 3 member tuple -> actor, message count, message arg factory.

    """
    return _do_increment_counter_1, ctx.args.user_accounts * ctx.args.increments, lambda: _yield_parameterizations(ctx)


def _yield_parameterizations(ctx: ExecutionContext) -> typing.Generator:
    """Yields parameterizations to be dispatched to actor via a message queue.
    
    """
    for account_index in range(constants.ACC_RUN_USERS, ctx.args.user_accounts + constants.ACC_RUN_USERS):
        for _ in range(0, ctx.args.increments):
            yield (ctx, account_index)


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
    verification.verify_deploy(ctx, block_hash, deploy_hash)
    
    # Pull account under which contract was installed.
    network = cache.infra.get_network(node_id.network)

    count = clx.contracts.counter_define_stored.get_count(node_id, network.faucet, block_hash)
    assert count == ctx.args.increments, "counter verification failed"


@dramatiq.actor(queue_name="workflows.generators.WG-200")
def _do_increment_counter_1(ctx: ExecutionContext, account_index: int):
    """Dispatches counter increment deploy.
    
    """
    # Set account.
    account = cache.state.get_account_by_index(ctx, account_index)

    # Increment on-chain.
    (node, deploy_hash) = clx.contracts.counter_define_stored.increment(ctx, account)

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
