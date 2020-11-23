import dramatiq

from stests import chain
from stests.chain.utils import DeployDispatchInfo
from stests.core import cache
from stests.core import factory
from stests.core.types.chain import Account
from stests.core.types.chain import AccountType
from stests.core.types.chain import DeployType
from stests.core.types.infra import Network
from stests.core.types.orchestration import ExecutionContext
from stests.generators.utils.infra import get_network_node



# Queue to which messages will be dispatched.
_QUEUE = "orchestration.generators.accounts"

# Account index: network faucet.
ACC_NETWORK_FAUCET_INDEX = 0

# Map of transfer types to handling functions.
TFR_TYPE_TO_TFR_FN = {
    DeployType.TRANSFER_WASM: chain.set_transfer_wasm,
    DeployType.TRANSFER_WASMLESS: chain.set_transfer_wasmless,
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
    :param transfer_type: Type of transfer to dispatch.
    
    """
    # Set target network / node.
    network, node = get_network_node(ctx)
    
    # Set counterparties.
    cp1 = get_account(ctx, network, cp1_index)
    cp2 = get_account(ctx, network, cp2_index)

    # Dispatch tx -> chain.
    deploy_type = DeployType[transfer_type]
    dispatch_fn = TFR_TYPE_TO_TFR_FN[deploy_type]
    dispatch_info = DeployDispatchInfo(cp1, network, node)
    deploy_hash, dispatch_duration, dispatch_attempts = dispatch_fn(dispatch_info, cp2, amount)

    # Update cache: deploy.
    cache.state.set_deploy(factory.create_deploy_for_run(
        ctx=ctx, 
        account=cp1,
        associated_account=cp2,
        node=node, 
        deploy_hash=deploy_hash, 
        dispatch_attempts=dispatch_attempts,
        dispatch_duration=dispatch_duration,
        typeof=deploy_type
        ))

    # Update cache: account balances.
    if cp1.is_run_account:
        cache.state.decrement_account_balance(cp1, amount)
    if cp2.is_run_account:
        cache.state.increment_account_balance(cp2, amount)


def get_account(ctx: ExecutionContext, network: Network, account_index: int) -> Account:
    """Returns either a faucet account or a user account.
    
    """
    # Faucet accounts.
    if account_index == ACC_NETWORK_FAUCET_INDEX:
        if not network.faucet:
            raise ValueError("Network faucet account does not exist.")
        return network.faucet

    # User accounts.
    return get_user_account(ctx, account_index)


def get_user_account(ctx: ExecutionContext, account_index: int) -> Account:
    """Returns either a faucet account or a user account.
    
    """
    return factory.create_account_for_run(ctx, account_index) 
