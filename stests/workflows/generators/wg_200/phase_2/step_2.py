import typing

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.types.chain import ContractType
from stests.core.types.chain import DeployType
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.core import factory
from stests.workflows.generators.utils import verification
from stests.workflows.generators.wg_200 import constants



# Step label.
LABEL = "invoke-increment"



def execute(ctx: ExecutionContext) -> typing.Union[dramatiq.Actor, int, typing.Callable]:
    """Step entry point.
    
    :param ctx: Execution context information.

    :returns: 3 member tuple -> actor, message count, message arg factory.

    """
    return _do_increment_counter_0, ctx.args.user_accounts * ctx.args.increments, lambda: _yield_parameterizations(ctx)


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
    deploy = verification.verify_deploy(ctx, block_hash, deploy_hash)
    account = cache.state.get_account_by_index(ctx, deploy.account_index)
    contract = clx.contracts.get_contract(ContractType.COUNTER_DEFINE)
    count = contract.get_count(node_id, account, block_hash)

    assert count == ctx.args.increments, "counter verification failed"


@dramatiq.actor(queue_name="workflows.generators.WG-200")
def _do_increment_counter_0(ctx: ExecutionContext, account_index: int):
    """Dispatches counter increment deploy.
    
    """
    # Set account.
    account = cache.state.get_account_by_index(ctx, account_index)

    # Set contract.
    contract = clx.contracts.get_contract(ContractType.COUNTER_DEFINE)

    # Dispatch contract execution deploy.
    (node, deploy_hash) = contract.increment(ctx, account)

    # Update cache.
    cache.state.set_deploy(factory.create_deploy_for_run(
        ctx=ctx, 
        account=account,
        node=node, 
        deploy_hash=deploy_hash, 
        typeof=DeployType.COUNTER_DEFINE
        ))
