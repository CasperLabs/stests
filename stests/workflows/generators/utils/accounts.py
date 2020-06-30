import typing

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core import factory
from stests.core.types.chain import Account
from stests.core.types.chain import ContractType
from stests.core.types.chain import DeployType
from stests.core.types.orchestration import ExecutionContext



# Queue to which messages will be dispatched.
_QUEUE = "workflows.generators.accounts"

# Account index: network faucet.
ACC_NETWORK_FAUCET = 0


@dramatiq.actor(queue_name=_QUEUE)
def do_transfer(
    ctx: ExecutionContext,
    cp1_index: int,
    cp2_index: int,
    amount: int = None,
    ):
    # Set counterparties.
    cp1 = _get_account(ctx, cp1_index)
    cp2 = _get_account(ctx, cp2_index)

    # Set amount for refunds.
    is_refund = amount is None
    if is_refund:
        cp1_balance = clx.get_account_balance(ctx, cp1.account_id)
        amount = cp1_balance - clx.CLX_TX_FEE
        if amount <= 0:
            raise ValueError(f"Counter party 1 (account={cp1.index}) does not have enough CLX to pay refund transaction fee, balance={cp1_balance}.")

    # Set contract.
    if ctx.run_type == "WG-100":
        contract = clx.contracts.get_contract(ContractType.TRANSFER_U512_WASM)
    elif ctx.run_type == "WG-110":
        contract = clx.contracts.get_contract(ContractType.TRANSFER_U512_STORED)
    elif ctx.run_type == "WG-120" and ctx.phase_index == 1:
        contract = clx.contracts.get_contract(ContractType.TRANSFER_U512_STORED)
    else:
        contract = clx.contracts.get_contract(ContractType.TRANSFER_U512)

    # Transfer CLX from cp1 -> cp2.    
    node, deploy_hash, dispatch_duration, dispatch_attempts = contract.transfer(ctx, cp1, cp2, amount)

    # Update cache: deploy.
    cache.state.set_deploy(factory.create_deploy_for_run(
        ctx=ctx, 
        account=cp1,
        node=node, 
        deploy_hash=deploy_hash, 
        dispatch_attempts=dispatch_attempts,
        dispatch_duration=dispatch_duration,
        typeof=DeployType.TRANSFER_REFUND if is_refund else DeployType.TRANSFER
        ))

    # Update cache: transfer.
    cache.state.set_transfer(factory.create_transfer(
        ctx=ctx,
        amount=amount,
        asset="CLX",
        cp1=cp1,
        cp2=cp2,
        deploy_hash=deploy_hash,
        ))

    # Update cache: account balances.
    if cp1.is_run_account:
        cache.state.decrement_account_balance(cp1, amount)
    if cp2.is_run_account:
        cache.state.increment_account_balance(cp2, amount)


def _get_account(ctx: ExecutionContext, account_index: int) -> Account:
    """Pulls & returns a cached account.
    
    """
    if account_index == ACC_NETWORK_FAUCET:
        network_id = factory.create_network_id(ctx.network)
        network = cache.infra.get_network(network_id)
        if not network.faucet:
            raise ValueError("Network faucet account does not exist.")
        return network.faucet
    else:
        return cache.state.get_account_by_index(ctx, account_index)           
