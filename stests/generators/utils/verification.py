from stests import chain
from stests.core import cache
from stests.core.types.chain import Account
from stests.core.types.chain import Deploy
from stests.core.types.chain import DeployStatus
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.core.types.orchestration import ExecutionAspect
from stests.core.utils.exceptions import IgnoreableAssertionError
from stests.generators.utils.infra import get_network_node
from stests.generators.utils.constants import ACC_RUN_USERS


def verify_deploy(ctx: ExecutionContext, block_hash: str, deploy_hash: str, expected_status=DeployStatus.ADDED) -> Deploy:
    """Verifies that a deploy is in a finalized state.
    
    """
    deploy = cache.state.get_deploy(ctx, deploy_hash)
    assert deploy, f"deploy could not be retrieved: {deploy_hash}"
    assert deploy.status == expected_status, f"deploy status is not {expected_status.name}"
    assert deploy.block_hash == block_hash, f"deploy block hash mismatch : block-hash={block_hash}"

    return deploy


def verify_deploy_count(ctx: ExecutionContext, expected: int, aspect: ExecutionAspect = ExecutionAspect.STEP):
    """Verifies that a step's count of finalized deploys tallies.
    
    """
    count = cache.orchestration.get_deploy_count(ctx, aspect) 
    assert count == expected, \
           IgnoreableAssertionError(f"deploy count mismatch: actual={count}, expected={expected}")


def verify_account_balance(ctx: ExecutionContext, account_index: int, expected: int) -> Account:
    """Verifies that an account balance is as per expectation.
    
    """
    account = cache.state.get_account_by_index(ctx, account_index)
    network, node = get_network_node(ctx)
    state_root_hash = chain.get_state_root_hash(network, node)

    purse_uref = chain.get_account_main_purse_uref(network, node, account.account_key, state_root_hash)
    assert purse_uref is not None, \
           f"account {account_index} main purse uref could not be retrieved - probably on-chain account does not exist"

    balance = chain.get_account_balance(network, node, purse_uref, state_root_hash)
    assert balance == expected, \
           f"account balance mismatch: account_index={account_index}, account_key={account.account_key}, expected={expected}, actual={balance}"


def verify_account_balance_on_transfer(
    ctx: ExecutionContext,
    node_id: NodeIdentifier,
    state_root_hash: str,
    account_index: int,
    expected: int,
    ) -> Account:
    """Verifies that an account balance is as per expectation.
    
    """
    # Set account.
    account = cache.state.get_account_by_index(ctx, account_index)

    # Set network / node in readiness for chain interaction.
    network, node = get_network_node(node_id)

    # Set account main purse uref.
    purse_uref = chain.get_account_main_purse_uref(network, node, account.account_key, state_root_hash)
    assert purse_uref is not None, \
           f"account {account_index} main purse uref could not be retrieved - probably on-chain account does not exist"

    # Set account balance.
    balance = chain.get_account_balance(network, node, purse_uref, state_root_hash)
    assert balance == expected, \
           f"account balance mismatch: account_index={account_index}, account_key={account.account_key}, expected={expected}, actual={balance}"

    return account


def verify_account_count(ctx: ExecutionContext) -> Deploy:
    """Verifies number of created accounts.
    
    """
    cached = cache.state.get_account_count(ctx)
    expected = ctx.args.user_accounts + 2
    assert cached == expected, f"cached account total mismatch: actual={cached}, expected={expected}."
