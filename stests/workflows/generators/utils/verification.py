from stests.core import cache
from stests.core import clx
from stests.core.domain import Account
from stests.core.domain import Deploy
from stests.core.domain import DeployStatus
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.core.orchestration import ExecutionAspect
from stests.core.domain import Transfer
from stests.core.domain import TransferStatus
from stests.core.utils.exceptions import IgnoreableAssertionError



def verify_deploy(ctx: ExecutionContext, block_hash: str, deploy_hash: str) -> Deploy:
    """Verifies that a deploy is in a finalized state.
    
    """
    deploy = cache.state.get_deploy(deploy_hash)
    assert deploy, f"deploy could not be retrieved: {deploy_hash}"
    assert deploy.status == DeployStatus.FINALIZED, f"deploy is not FINALIZED : {deploy_hash}"
    assert deploy.block_hash == block_hash, f"finalized deploy block hash mismatch : block-hash={block_hash}"

    return deploy


def verify_deploy_count(ctx: ExecutionContext, expected: int, aspect: ExecutionAspect = ExecutionAspect.STEP):
    """Verifies that a step's count of finalized deploys tallies.
    
    """
    count = cache.orchestration.get_deploy_count(ctx, aspect) 
    assert count == expected, IgnoreableAssertionError(f"deploy count mismatch: actual={count}, expected={expected}")


def verify_transfer(ctx: ExecutionContext, block_hash: str, deploy_hash: str) -> Transfer:
    """Verifies that a transfer between counter-parties completed.
    
    """
    transfer = cache.state.get_transfer(deploy_hash)
    assert transfer, f"transfer could not be retrieved: {deploy_hash}"
    assert transfer.status == TransferStatus.COMPLETE, f"transfer is not COMPLETE : {deploy_hash}"

    return transfer


def verify_account_balance(ctx: ExecutionContext, node_id: NodeIdentifier, block_hash: str, account_index: int, expected: int) -> Account:
    """Verifies that an account balance is as per expectation.
    
    """
    account = cache.state.get_account_by_index(ctx, account_index)
    assert account, f"account {account_index} could not be retrieved"

    balance = clx.get_balance(node_id, account, block_hash=block_hash)
    assert balance == expected, f"account balance mismatch: account_index={account_index}, actual={balance}, expected={expected}"

    return account
