import typing

import dramatiq

from stests import chain
from stests.core import cache
from stests.core import factory
from stests.core.types.chain import Account
from stests.core.types.chain import ContractType
from stests.core.types.chain import DeployType
from stests.core.types.chain import TransferType
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.types.orchestration import ExecutionAspect
from stests.core.types.orchestration import ExecutionContext
from stests.orchestration.generators.utils.infra import get_network_node



# Queue to which messages will be dispatched.
_QUEUE = "orchestration.generators.accounts"

# Account index: network faucet.
ACC_NETWORK_FAUCET_INDEX = 0

# Map of transfer types to handling functions.
TFR_TYPE_TO_TFR_FN = {
    TransferType.WASM_PER_DEPLOY: chain.set_transfer_wasm,
    TransferType.WASMLESS: chain.set_transfer_wasmless,
}


@dramatiq.actor(queue_name=_QUEUE)
def do_transfer(
    ctx: ExecutionContext,
    cp1_index: int,
    cp2_index: int,
    amount: int,
    transfer_type: str,
    ):
    """Executes a wasm-vased account token transfer between counter-parties.

    :param ctx: Execution context information.
    :param cp1_index: Account index of counter-party 1.
    :param cp2_index: Account index of counter-party 1.
    :param amount: Amount (in motes) to transfer.
    :param chain_transfer_fn: Target chain transfer function.
    
    """
    # Set target network / node.
    network, node = get_network_node(ctx)
    
    # Set counterparties.
    cp1 = get_account(ctx, network, cp1_index)
    cp2 = get_account(ctx, network, cp2_index)

    # Dispatch tx -> chain.
    deploy_hash, dispatch_duration, dispatch_attempts = TFR_TYPE_TO_TFR_FN[TransferType[transfer_type]](
        network,
        node,
        cp1,
        cp2,
        amount,
    )

    # Update cache: deploy.
    cache.state.set_deploy(factory.create_deploy_for_run(
        ctx=ctx, 
        account=cp1,
        node=node, 
        deploy_hash=deploy_hash, 
        dispatch_attempts=dispatch_attempts,
        dispatch_duration=dispatch_duration,
        typeof=DeployType.TRANSFER
        ))

    # Update cache: transfer.
    cache.state.set_transfer(factory.create_transfer(
        ctx=ctx,
        amount=amount,
        asset="CSPR",
        cp1=cp1,
        cp2=cp2,
        deploy_hash=deploy_hash,
        ))
    
    # Increment deploy counts.
    # Note: this is temporary until we can increment during deploy finalisation.
    cache.orchestration.increment_deploy_counts(ctx)


def get_account(ctx: ExecutionContext, network: Network, account_index: int) -> Account:
    """Pulls & returns a cached account.
    
    """
    if account_index == ACC_NETWORK_FAUCET_INDEX:
        if not network.faucet:
            raise ValueError("Network faucet account does not exist.")
        return network.faucet
    else:
        return cache.state.get_account_by_index(ctx, account_index)   
