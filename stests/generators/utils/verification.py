from stests.core import cache
from stests.core import clx
from stests.core.domain import DeployStatus
from stests.core.orchestration import ExecutionContext
from stests.core.orchestration import ExecutionAspect
from stests.core.domain import Transfer
from stests.core.domain import TransferStatus



def verify_deploy(ctx: ExecutionContext, bhash: str, dhash: str):
    """Verifies that a deploy is in a finalized state.
    
    """
    deploy = cache.state.get_deploy(dhash)
    assert deploy, f"deploy could not be retrieved: {dhash}"
    assert deploy.status == DeployStatus.FINALIZED, f"deploy is not FINALIZED : {dhash}"

    return deploy


def verify_deploy_count(ctx: ExecutionContext, expected: int, aspect: ExecutionAspect = ExecutionAspect.STEP):
    """Verifies that a step's count of finalized deploys tallies.
    
    """
    count = cache.orchestration.get_deploy_count(ctx, aspect) 
    assert count == expected, f"deploy count mismatch: actual={count}, expected={expected}"


def verify_transfer(ctx: ExecutionContext, dhash: str) -> Transfer:
    """Verifies that a transfer between counter-parties completed.
    
    """
    transfer = cache.state.get_transfer(dhash)
    assert transfer, f"transfer could not be retrieved: {dhash}"
    assert transfer.status == TransferStatus.COMPLETE, f"transfer is not COMPLETE : {dhash}"

    return transfer


def verify_account_balance(ctx: ExecutionContext, account_index: int, expected: int):
    """Verifies that an account balance is as per expectation.
    
    """
    account = cache.state.get_account_by_index(ctx, account_index)
    assert account, f"account {account_index} could not be retrieved"

    balance = clx.get_balance(ctx, account)
    assert clx.get_balance(ctx, account) == expected, \
           f"account balance mismatch: account_index={account_index}, actual={balance}, expected={expected}"

    return account
