import typing
import dramatiq

from stests import chain
from stests.core import cache
from stests.core import factory
from stests.core.types.chain import Account
from stests.core.types.chain import AccountType
from stests.core.types.chain import DeployType
from stests.core.types.infra import Node
from stests.core.types.infra import Network
from stests.core.types.orchestration import ExecutionContext
from stests.generators.utils import constants
from stests.generators.utils.infra import get_network_node



# Queue to which messages will be dispatched.
_QUEUE = "orchestration.generators.accounts"

# Account index: network faucet.
ACC_NETWORK_FAUCET_INDEX = 0

# Map of transfer types to handling functions.
TFR_TYPE_TO_TFR_FN = {
    DeployType.TRANSFER_WASM: chain.set_transfer_wasm,
    DeployType.TRANSFER_NATIVE: chain.set_transfer_native,
}


@dramatiq.actor(queue_name=_QUEUE)
def do_refund(
    ctx: ExecutionContext,
    cp1_index: int,
    cp2_index: int,
    transfer_type: str,
    ):
    """Executes a token refund between 2 counter-parties.

    :param ctx: Execution context information.
    :param cp1_index: Account index of counter-party 1.
    :param cp2_index: Account index of counter-party 1.
    :param transfer_type: Type of transfer to dispatch.
    
    """
    do_transfer(ctx, cp1_index, cp2_index, None, transfer_type)


@dramatiq.actor(queue_name=_QUEUE)
def do_transfer(
    ctx: ExecutionContext,
    cp1_index: int,
    cp2_index: int,
    amount: int,
    transfer_type: str,
    ):
    """Executes a token transfer between 2 counter-parties.

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

    # Set amount to transfer (in the case of refunds).
    if amount is None:
        amount = get_account_balance(network, node, cp1) - chain.DEFAULT_TX_FEE

    # Dispatch tx -> chain.
    dispatch_info = chain.DeployDispatchInfo(cp1, network, node)
    dispatch_fn = TFR_TYPE_TO_TFR_FN[DeployType[transfer_type]]
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
        typeof=DeployType[transfer_type]
        ))

    # Update cache: account balances.
    if cp1.is_run_account:
        cache.state.decrement_account_balance(cp1, amount)
    if cp2.is_run_account:
        cache.state.increment_account_balance(cp2, amount)

   
def do_transfer_fire_forget(
    ctx: ExecutionContext,
    cp2: Account,
    amount: int,
    transfer_type: DeployType,
    ):
    """Executes fire & forget token transfers between counter-parties.

    :param ctx: Execution context information.
    :param cp2: Counter-party 2 account.
    :param amount: Amount (in motes) to transfer.
    :param transfer_type: Type of transfer to dispatch.
    
    """
    network, node = get_network_node(ctx)
    cp1 = get_account(ctx, network, get_account_idx_for_network_faucet())
    dispatch_info = chain.DeployDispatchInfo(cp1, network, node)
    dispatch_fn = TFR_TYPE_TO_TFR_FN[transfer_type]
    dispatch_fn(dispatch_info, cp2, amount)

    cache.orchestration.increment_deploy_counts(ctx, 1)


def get_account(ctx: ExecutionContext, network: Network, account_index: int) -> Account:
    """Returns either a faucet account or a user account.
    
    """
    # Faucet accounts.
    if account_index == ACC_NETWORK_FAUCET_INDEX:
        if not network.faucet:
            raise ValueError("Network faucet account does not exist.")
        return network.faucet

    # Cached accounts.
    if account_index > 0:
        return cache.state.get_account_by_index(ctx, account_index)  

    # On the fly accounts.
    return factory.create_account_for_run(ctx, account_index)


def get_account_balance(network: Network, node: Node, account: Account) -> int:
    """Returns either a faucet account or a user account.
    
    """
    purse_uref = chain.get_account_main_purse_uref(network, node, account.account_key)

    return chain.get_account_balance(network, node, purse_uref)


def get_account_idx_for_deploy(accounts: int, deploy_idx: int) -> int:
    """Returns account index to use for a particular transfer.
    
    :param accounts: Number of accounts within batch.
    :param deploy_idx: Index of deploy within batch.
    :returns: Ordinal index of account used to dispatch deploy.

    """
    return deploy_idx if accounts == 0 else \
           deploy_idx % accounts or accounts


def get_account_idx_for_network_faucet() -> int:
    """Returns network specific faucet account index.
    
    :returns: Ordinal index of account acting as network faucet.

    """ 
    return constants.ACC_NETWORK_FAUCET


def get_account_idx_for_run_faucet(accounts: int, deploys: int) -> int:
    """Returns run specific faucet account index when dispatching a deploy batch.
    
    :param accounts: Number of accounts within batch.
    :param deploys: Number of deploys within batch.
    :returns: Ordinal index of account acting as run faucet.

    """ 
    return (deploys if accounts == 0 else accounts) + 1


def get_account_range(accounts: int, deploys: int) -> int:
    """Returns run specific faucet account index whcn dispatching a deploy batch.
    
    :param accounts: Number of accounts within batch.
    :param deploys: Number of deploys within batch.
    :returns: Ordinal index of account acting as run faucet.

    """ 
    return range(1, (deploys if accounts == 0 else accounts) + 1)


def get_account_set(ctx: ExecutionContext, accounts: int, deploys: int) -> int:
    """Returns run specific faucet account index whcn dispatching a deploy batch.
    
    :param ctx: Execution context information.
    :param accounts: Number of accounts within batch.
    :param deploys: Number of deploys within batch.
    :returns: Set of accounts to act as transfer targets.

    """ 
    account_range = range(deploys) if accounts == 0 else range(accounts)

    return [factory.create_account_for_run(ctx, i  + 1) for i in account_range]


def get_account_deploy_count(accounts: int, account_idx: int, deploys: int) -> int:
    """Returns account index to use for a particular transfer.
    
    """
    if accounts == 0:
        return 1

    q, r = divmod(deploys, accounts)

    return q + (1 if account_idx <= r else 0)


def get_faucet_initial_balance(transfers, amount) -> int:
    """Returns initial faucet account CSPR balance.
    
    """
    return (transfers * amount) + (((2 * transfers) + 1) * chain.DEFAULT_TX_FEE)
