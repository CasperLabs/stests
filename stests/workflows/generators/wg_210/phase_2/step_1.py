import typing

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.types.chain import ContractType
from stests.core.types.chain import DeployType
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.core import factory
from stests.workflows.generators.utils import constants
from stests.workflows.generators.utils import verification



# Step label.
LABEL = "invoke-wasm"


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

    contract = clx.contracts.get_contract(ContractType.COUNTER_DEFINE)
    contract_account = cache.state.get_account_by_index(ctx, constants.ACC_RUN_CONTRACT)
    count = contract.get_count(ctx, contract_account)
    assert count == ctx.args.user_accounts * ctx.args.increments, "counter verification failed"


def verify_deploy(ctx: ExecutionContext, node_id: NodeIdentifier, block_hash: str, deploy_hash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param node_id: Identifier of node which emitted block finalisation event.
    :param block_hash: A finalized block hash.
    :param deploy_hash: A finalized deploy hash.

    """
    verification.verify_deploy(ctx, block_hash, deploy_hash)


@dramatiq.actor(queue_name="workflows.generators.WG-210")
def _do_increment_counter_1(ctx: ExecutionContext, account_index: int):
    """Dispatches counter increment deploy.
    
    """
    # Set contract info.
    contract = clx.contracts.get_contract(ContractType.COUNTER_DEFINE_STORED)
    contract_account = cache.state.get_account_by_index(ctx, constants.ACC_RUN_CONTRACT)
    contract_keys = cache.state.get_named_keys(ctx, contract_account, ContractType.COUNTER_DEFINE_STORED)

    # Set user account.
    user_account = cache.state.get_account_by_index(ctx, account_index)

    # Increment on-chain counter.
    node, deploy_hash, dispatch_time = contract.increment(ctx, contract_account, contract_keys, user_account)

    # Update cache.
    cache.state.set_deploy(factory.create_deploy_for_run(
        ctx=ctx, 
        account=user_account,
        node=node, 
        deploy_hash=deploy_hash, 
        dispatch_time=dispatch_time,
        typeof=DeployType.COUNTER_DEFINE
        ))
