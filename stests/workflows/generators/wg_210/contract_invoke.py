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



# Target smart contract.
CONTRACT = clx.contracts.counter_define_stored

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
    print(222)


@dramatiq.actor(queue_name="workflows.generators.WG-210")
def _do_increment_counter_1(ctx: ExecutionContext, account_index: int):
    """Dispatches counter increment deploy.
    
    """
    # Set accounts.
    account_contract = cache.state.get_account_by_index(ctx, constants.ACC_RUN_CONTRACT)
    account_user = cache.state.get_account_by_index(ctx, account_index)

    # Set named keys.
    # Set named keys of stored contract + slot.
    named_keys = clx.get_account_named_keys(ctx, account_contract, filter_keys=CONTRACT.NAMED_KEYS)
    named_keys = {i.name: i.key.hash.hash.hex() for i in named_keys}
    


    # Increment on-chain.
    (node, deploy_hash) = CONTRACT.increment(ctx, account_contract, account_user)

    # Set info. 
    deploy = factory.create_deploy_for_run(
        account=account_user,
        ctx=ctx, 
        node=node, 
        deploy_hash=deploy_hash, 
        typeof=DeployType.COUNTER_DEFINE
        )

    # Update cache.
    cache.state.set_deploy(deploy)
