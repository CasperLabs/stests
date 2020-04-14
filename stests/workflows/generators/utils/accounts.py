import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.domain import AccountType
from stests.core.domain import ContractType
from stests.core.domain import DeployType
from stests.core.domain import Node
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.core.utils import factory



# Queue to which messages will be dispatched.
_QUEUE = "workflows.generators.accounts"

# Account index: network faucet.
ACC_NETWORK_FAUCET = 0


@dramatiq.actor(queue_name=_QUEUE)
def do_create_account(ctx: ExecutionContext, index: int, typeof: AccountType):
    """Creates an account for use during the course of a simulation.

    :param ctx: Execution context information.
    :param index: Run specific account index.
    :param typeof: Account type.

    """
    account = factory.create_account_for_run(ctx, index=index, typeof=typeof)
    cache.state.set_account(account)


@dramatiq.actor(queue_name=_QUEUE)
def do_fund_account(
    ctx: ExecutionContext,
    cp1_index: int,
    cp2_index: int,
    amount: int,
    use_stored_contract: bool
    ):
    """Funds an account by transfering CLX transfer between 2 counterparties.

    :param ctx: Execution context information.
    :param cp1_index: Run specific account index of counter-party one.
    :param cp2_index: Run specific account index of counter-party two.
    :param amount: Amount to be transferred.
    :param use_stored_contract: Flag indicating whether to use stored contract.
    
    """
    # Set counterparties.
    if cp1_index == ACC_NETWORK_FAUCET:
        network = cache.infra.get_network_by_ctx(ctx)
        if not network.faucet:
            raise ValueError("Network faucet account does not exist.")
        cp1 = network.faucet
    else:
        cp1 = cache.state.get_account_by_index(ctx, cp1_index)
    cp2 = cache.state.get_account_by_index(ctx, cp2_index)
    
    # Set contract.
    transfer = clx.contracts.transfer_U512_stored if use_stored_contract else clx.contracts.transfer_U512

    # Transfer CLX from cp1 -> cp2.    
    (node, deploy_hash) = transfer.execute(ctx, cp1, cp2, amount)

    # Set info. 
    deploy = factory.create_deploy_for_run(
        account=cp1,
        ctx=ctx, 
        node=node, 
        deploy_hash=deploy_hash, 
        typeof=DeployType.TRANSFER
        )
    transfer = factory.create_transfer(
        ctx=ctx,
        amount=amount,
        asset="CLX",
        cp1=cp1,
        cp2=cp2,
        deploy_hash=deploy_hash,
        is_refundable=True
        )

    # Update cache.
    cache.state.set_deploy(deploy)
    cache.state.set_transfer(transfer)

    # Perform deploy verification - with 10 minute delay.
    # do_fund_account_verify_deploy_processing.send_with_options(
    #     args=(
    #         node, deploy_hash, ctx, cp1_index, cp2_index, amount, use_stored_contract
    #     ),
    #     delay=int(1e3 * 10)
    # )


@dramatiq.actor(queue_name=_QUEUE)
def do_fund_account_verify_deploy_processing(
    node: Node,
    deploy_hash: str,
    ctx: ExecutionContext,
    cp1_index: int,
    cp2_index: int,
    amount: int,
    use_stored_contract: bool
    ):
    print(f"TODO: perform post deploy dispatch verification: {node.address} {deploy_hash}")


@dramatiq.actor(queue_name=_QUEUE)
def do_refund(ctx: ExecutionContext, cp1_index: int, cp2_index: int, use_stored_contract: bool):
    """Performs a refund ot funds between 2 counterparties.

    :param ctx: Execution context information.
    :param cp1_index: Run specific account index of counter-party one.
    :param cp2_index: Run specific account index of counter-party two.
    :param use_stored_contract: Flag indicating whether to use stored contract.
    
    """
    # Set counterparties.
    cp1 = cache.state.get_account_by_index(ctx, cp1_index)
    if cp2_index == ACC_NETWORK_FAUCET:
        network = cache.infra.get_network_by_ctx(ctx)
        if not network.faucet:
            raise ValueError("Network faucet account does not exist.")
        cp2 = network.faucet
    else:
        cp2 = cache.state.get_account_by_index(ctx, cp2_index)

    # Set contract.
    transfer = clx.contracts.transfer_U512_stored if use_stored_contract else clx.contracts.transfer_U512

    # Refund CLX from cp1 -> cp2.
    (node, deploy_hash, amount) = transfer.execute_refund(ctx, cp1, cp2)

    # Set info. 
    deploy = factory.create_deploy_for_run(
        account=cp1,
        ctx=ctx, 
        node=node, 
        deploy_hash=deploy_hash, 
        typeof=DeployType.TRANSFER_REFUND
        )
    transfer = factory.create_transfer(
        ctx=ctx,
        amount=amount,
        asset="CLX",
        cp1=cp1,
        cp2=cp2,
        deploy_hash=deploy_hash,
        is_refundable=True
        )

    # Update cache.
    cache.state.set_deploy(deploy)
    cache.state.set_transfer(transfer)
