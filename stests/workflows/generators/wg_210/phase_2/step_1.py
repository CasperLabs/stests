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
from stests.workflows.generators.wg_210 import constants



# Step description.
DESCRIPTION = "Dispatches a notification to signal that generator has completed."

# Step label.
LABEL = "counter-call"


def execute(ctx: ExecutionContext) -> typing.Callable:
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    def get_messages():
        for account_index in range(constants.ACC_RUN_USERS, ctx.args.user_accounts + constants.ACC_RUN_USERS):
            for _ in range(0, ctx.args.increments):
                yield do_increment_counter_1.message(ctx, account_index)

    return get_messages


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    verification.verify_deploy_count(ctx, ctx.args.user_accounts * ctx.args.increments)    


def verify_deploy(ctx: ExecutionContext, node_id: NodeIdentifier, bhash: str, dhash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param bhash: A block hash.
    :param dhash: A deploy hash.

    """
    deploy = verification.verify_deploy(ctx, bhash, dhash)
    _verify_counter(ctx, deploy.account_index, bhash)


def _verify_counter(ctx: ExecutionContext, account_index: int, bhash: str):
    """Verfies that a counter has been incremented the correct number of times. 
    
    :param ctx: Execution context information.
    :param bhash: A block hash.

    """
    account = cache.state.get_account_by_index(ctx, account_index)
    _, client = clx.get_client(ctx)

    state = client.queryState(bhash, account.public_key, "counter/count", "address")
    assert state.cl_value.value.i32 == ctx.args.increments


@dramatiq.actor(queue_name=constants.TYPE)
def do_increment_counter_1(ctx: ExecutionContext, account_index: int):
    """Dispatches counter increment deploy.
    
    """
    # Set account.
    account = cache.state.get_account_by_index(ctx, account_index)

    # Set contract.
    contract = cache.infra.get_contract(ctx, ContractType.COUNTER_DEFINE)

    # Set args.
    session_args = ABI.args([
        ABI.string_value("target", "counter_inc")
        ])

    # Dispatch deploy.
    node, client = clx.get_client(ctx)
    dhash = client.deploy(
        session_args=session_args,
        session_hash=contract.hash_as_bytes,
        from_addr=account.public_key,
        private_key=account.private_key_as_pem_filepath,
        # TODO: allow these to be passed in via standard arguments
        payment_amount=clx.CLX_TX_FEE,
        gas_price=clx.CLX_TX_GAS_PRICE
    )
    logger.log(f"PYCLX :: counter-increment :: deploy-hash={dhash}")

    # Set info. 
    deploy = factory.create_deploy_for_run(
        account=account,
        ctx=ctx, 
        node=node, 
        deploy_hash=dhash, 
        typeof=DeployType.COUNTER_DEFINE
        )

    # Update cache.
    cache.state.set_deploy(deploy)
