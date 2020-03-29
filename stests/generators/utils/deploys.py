import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.domain import AccountType
from stests.core.domain import ContractType
from stests.core.domain import DeployType
from stests.core.domain import ContractType
from stests.core.orchestration import ExecutionContext
from stests.generators.utils import constants
from stests.core.utils import factory



# Queue to which messages will be dispatched.
_QUEUE = "orchestration.utils"


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
    if cp1_index == constants.ACC_NETWORK_FAUCET:
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
    (node, dhash) = transfer.execute(ctx, cp1, cp2, amount)

    # Set info. 
    deploy = factory.create_deploy_for_run(
        account=cp1,
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
    cache.state.set_deploy(deploy)
    cache.state.set_transfer(transfer)


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
    if cp2_index == constants.ACC_NETWORK_FAUCET:
        network = cache.infra.get_network_by_ctx(ctx)
        if not network.faucet:
            raise ValueError("Network faucet account does not exist.")
        cp2 = network.faucet
    else:
        cp2 = cache.state.get_account_by_index(ctx, cp2_index)

    # Set client contract.
    contract = None if not use_stored_contract else \
               cache.infra.get_contract(ctx, ContractType.TRANSFER_U512_STORED)

    # Set contract.
    transfer = clx.contracts.transfer_U512_stored if use_stored_contract else clx.contracts.transfer_U512

    # Refund CLX from cp1 -> cp2.
    (node, dhash, amount) = transfer.execute_refund(ctx, cp1, cp2)

    # Set info. 
    deploy = factory.create_deploy_for_run(
        account=cp1,
        ctx=ctx, 
        node=node, 
        deploy_hash=dhash, 
        typeof=DeployType.TRANSFER_REFUND
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
    cache.state.set_deploy(deploy)
    cache.state.set_transfer(transfer)


@dramatiq.actor(queue_name=_QUEUE)
def do_set_contract(
    ctx: ExecutionContext,
    account_index: int,
    contract_type: ContractType
    ):
    """Deploys a contract under a known account.

    :param ctx: Execution context information.
    :param account_index: Index of account to which a contract will be deployed.
    :param contract_type: Type of contract to deploy.
    
    """
    # Pull account info.
    account = cache.state.get_account_by_index(ctx, account_index)

    # Deploy contract.
    (node, deploy_hash) = clx.contracts.install_named(ctx, account, contract_type)

    # Set info. 
    deploy = factory.create_deploy_for_run(
        account=account,
        ctx=ctx, 
        node=node, 
        deploy_hash=deploy_hash, 
        typeof=DeployType.CONTRACT_INSTALL
        )

    # Update cache.
    cache.state.set_deploy(deploy)
