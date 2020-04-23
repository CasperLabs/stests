import typing

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.clx.defaults import CLX_TX_FEE
from stests.core.types.chain import Account
from stests.core.types.chain import AccountType
from stests.core.types.chain import ContractType
from stests.core.types.chain import DeployType
from stests.core.types.infra import Node
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.core import factory



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
    ):
    """Funds an account by transfering CLX transfer between 2 counterparties.

    :param ctx: Execution context information.
    :param cp1_index: Run specific account index of counter-party one.
    :param cp2_index: Run specific account index of counter-party two.
    :param amount: Amount to be transferred.
    
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
    contract_type = ContractType.TRANSFER_U512 if ctx.use_client_contract_for_transfers else ContractType.TRANSFER_U512_STORED
    contract = clx.contracts.get_contract(contract_type)

    # Transfer CLX from cp1 -> cp2.    
    node, deploy_hash = contract.transfer(ctx, cp1, cp2, amount)

    # Update cache.
    cache.state.set_deploy(factory.create_deploy_for_run(
        ctx=ctx, 
        account=cp1,
        node=node, 
        deploy_hash=deploy_hash, 
        typeof=DeployType.TRANSFER
        ))
    cache.state.set_transfer(factory.create_transfer(
        ctx=ctx,
        amount=amount,
        asset="CLX",
        cp1=cp1,
        cp2=cp2,
        deploy_hash=deploy_hash,
        ))


@dramatiq.actor(queue_name=_QUEUE)
def do_refund(ctx: ExecutionContext, cp1_index: int, cp2_index: int):
    """Performs a refund ot funds between 2 counterparties.

    :param ctx: Execution context information.
    :param cp1_index: Run specific account index of counter-party one.
    :param cp2_index: Run specific account index of counter-party two.
    
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
    contract_type = ContractType.TRANSFER_U512 if ctx.use_client_contract_for_transfers else ContractType.TRANSFER_U512_STORED
    contract = clx.contracts.get_contract(contract_type)

    # Refund CLX from cp1 -> cp2.
    node, deploy_hash, amount = _refund(ctx, cp1, cp2, contract)

    # Update cache.
    cache.state.set_deploy(factory.create_deploy_for_run(
        ctx=ctx, 
        account=cp1,
        node=node, 
        deploy_hash=deploy_hash, 
        typeof=DeployType.TRANSFER_REFUND
        ))
    cache.state.set_transfer(factory.create_transfer(
        ctx=ctx,
        amount=amount,
        asset="CLX",
        cp1=cp1,
        cp2=cp2,
        deploy_hash=deploy_hash,
        ))


def _refund(
    ctx: ExecutionContext,
    cp1: Account,
    cp2: Account,
    contract: typing.Callable
    ) -> typing.Tuple[Node, str, int]:
    """Executes a refund between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Execution context information.
    :param cp1: Account information of counter party 1.
    :param cp2: Account information of counter party 2.
    :param contract: Transfer contract to be invoked.

    :returns: 3 member tuple: dispatch node, deploy hash, refund amount.

    """
    # If amount is unspecified, set amount to entire balance.
    balance = clx.get_account_balance(ctx, cp1) 
    amount = balance - CLX_TX_FEE
    
    # Escape if cp1 has insufficient funds.
    if amount <= 0:
        logger.log_warning(f"Counter party 1 (account={cp1.index}) does not have enough CLX to pay refund transaction fee, balance={balance}.")
        return

    # Transfer funds.
    (node, deploy_hash) = contract.transfer(ctx, cp1, cp2, amount)

    return node, deploy_hash, amount
