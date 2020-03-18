import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.domain import ClientContractType
from stests.core.domain import DeployType
from stests.core.orchestration import ExecutionContext
from stests.core.utils import factory
from stests.generators.wg_100 import constants



# Queue to which messages will be dispatched.
_QUEUE = "orchestration.utils"


@dramatiq.actor(queue_name=_QUEUE)
def do_fund_account(ctx: ExecutionContext, cp1_index: int, cp2_index: int, amount: int):
    """Funds an account by transfering CLX transfer between 2 counterparties.

    :param ctx: Execution context information.
    :param cp1_index: Run specific account index of counter-party one.
    :param cp2_index: Run specific account index of counter-party two.
    :param amount: Amount to be transferred.
    
    """
    # Set counterparties.
    if cp1_index == constants.ACC_NETWORK_FAUCET:
        network = cache.orchestration.get_run_network(ctx)
        if not network.faucet:
            raise ValueError("Network faucet account does not exist.")
        cp1 = network.faucet
    else:
        cp1 = cache.state.get_account_by_run(ctx, cp1_index)
    cp2 = cache.state.get_account_by_run(ctx, cp2_index)
    
    # Set client contract.
    contract = None if not ctx.use_stored_contracts else \
               cache.infra.get_client_contract(ctx, ClientContractType.TRANSFER_U512_STORED)

    # Transfer CLX from cp1 -> cp2.    
    (node, dhash) = clx.do_transfer(ctx, cp1, cp2, amount, contract)

    # Set info. 
    deploy = factory.create_deploy_for_run(
        ctx=ctx, 
        node=node, 
        deploy_hash=dhash, 
        typeof=DeployType.TRANSFER
        )
    transfer = factory.create_transfer(
        ctx=ctx,
        amount=amount,
        asset="CLX",
        cp1=cp1,
        cp2=cp2,
        deploy_hash=dhash,
        is_refundable=True
        )

    # Update cache.
    cache.state.set_run_deploy(deploy)
    cache.state.set_run_transfer(transfer)


@dramatiq.actor(queue_name=_QUEUE)
def do_refund(ctx: ExecutionContext, cp1_index: int, cp2_index: int):
    """Performs a refund ot funds between 2 counterparties.

    :param ctx: Execution context information.
    :param cp1_index: Run specific account index of counter-party one.
    :param cp2_index: Run specific account index of counter-party two.
    
    """
    # Set counterparties.
    cp1 = cache.state.get_account_by_run(ctx, cp1_index)
    if cp2_index == constants.ACC_NETWORK_FAUCET:
        network = cache.orchestration.get_run_network(ctx)
        if not network.faucet:
            raise ValueError("Network faucet account does not exist.")
        cp2 = network.faucet
    else:
        cp2 = cache.state.get_account_by_run(ctx, cp2_index)

    # Set client contract.
    contract = None if not ctx.use_stored_contracts else \
               cache.infra.get_client_contract(ctx, ClientContractType.TRANSFER_U512_STORED)

    # Refund CLX from cp1 -> cp2.
    (node, dhash, amount) = clx.do_refund(ctx, cp1, cp2, contract=contract)

    # Set info. 
    deploy = factory.create_deploy_for_run(
        ctx=ctx, 
        node=node, 
        deploy_hash=dhash, 
        typeof=DeployType.REFUND
        )
    transfer = factory.create_transfer(
        ctx=ctx,
        amount=amount,
        asset="CLX",
        cp1=cp1,
        cp2=cp2,
        deploy_hash=dhash,
        is_refundable=True
        )

    # Update cache.
    cache.state.set_run_deploy(deploy)
    cache.state.set_run_transfer(transfer)
