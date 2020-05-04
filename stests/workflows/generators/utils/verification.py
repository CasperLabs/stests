from stests.core import cache
from stests.core import clx
from stests.core.types.chain import Account
from stests.core.types.chain import Deploy
from stests.core.types.chain import DeployStatus
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.core.types.orchestration import ExecutionAspect
from stests.core.types.chain import Transfer
from stests.core.types.chain import TransferStatus
from stests.core.utils.exceptions import IgnoreableAssertionError
from stests.workflows.generators.utils.constants import ACC_RUN_USERS



def verify_deploy(ctx: ExecutionContext, block_hash: str, deploy_hash: str) -> Deploy:
    """Verifies that a deploy is in a finalized state.
    
    """
    deploy = cache.state.get_deploy(ctx, deploy_hash)
    assert deploy, "deploy could not be retrieved"
    assert deploy.status == DeployStatus.FINALIZED, "deploy is not FINALIZED"
    assert deploy.block_hash == block_hash, f"finalized deploy block hash mismatch : block-hash={block_hash}"

    return deploy


def verify_deploy_count(ctx: ExecutionContext, expected: int, aspect: ExecutionAspect = ExecutionAspect.STEP):
    """Verifies that a step's count of finalized deploys tallies.
    
    """
    count = cache.orchestration.get_deploy_count(ctx, aspect) 
    assert count == expected, IgnoreableAssertionError(f"deploy count mismatch: actual={count}, expected={expected}")


def verify_transfer(ctx: ExecutionContext, node_id: NodeIdentifier, block_hash: str, deploy_hash: str) -> Transfer:
    """Verifies that a transfer between counter-parties completed.
    
    """
    transfer = cache.state.get_transfer_by_ctx(ctx, deploy_hash)
    assert transfer, "transfer could not be retrieved"
    assert transfer.status == TransferStatus.COMPLETE, "transfer is not COMPLETE"

    _verify_account_balance(ctx, node_id, block_hash, transfer.cp1_index)
    _verify_account_balance(ctx, node_id, block_hash, transfer.cp2_index)


def _verify_account_balance(ctx: ExecutionContext, node_id: NodeIdentifier, block_hash: str, account_index: int, verify_user_accounts_only: bool = True) -> Account:
    """Verifies that an account balance is as per expectation.
    
    """
    # Only verify user accounts as these are guaranteed to be verifiable.
    if verify_user_accounts_only and account_index < ACC_RUN_USERS:
        return
    
    account = cache.state.get_account_by_index(ctx, account_index)
    assert account, f"account {account_index} could not be retrieved"

    expected = cache.state.get_account_balance(account)
    actual = clx.get_account_balance(node_id, account.public_key, block_hash=block_hash)
    assert actual == expected, f"account balance mismatch: account_index={account_index}, actual={actual}, expected={expected}"
