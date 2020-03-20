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
    assert deploy
    assert deploy.status == DeployStatus.FINALIZED

    return deploy


def verify_deploy_count(ctx: ExecutionContext, expected: int, aspect: ExecutionAspect = ExecutionAspect.STEP):
    """Verifies that a step's count of finalized deploys tallies.
    
    """
    assert cache.orchestration.get_deploy_count(ctx, aspect) == expected


def verify_refund(ctx: ExecutionContext, dhash: str) -> Transfer:
    """Verifies that a refund between counter-parties completed.
    
    """
    refund = cache.state.get_transfer(dhash)
    assert refund
    assert refund.status == TransferStatus.COMPLETE

    return refund


def verify_transfer(ctx: ExecutionContext, dhash: str) -> Transfer:
    """Verifies that a transfer between counter-parties completed.
    
    """
    transfer = cache.state.get_transfer(dhash)
    assert transfer
    assert transfer.status == TransferStatus.COMPLETE

    return transfer


def verify_account_balance(ctx: ExecutionContext, account_index: int, expected: int):
    """Verifies that an account balance is as per expectation.
    
    """
    account = cache.state.get_account_by_index(ctx, account_index)
    assert account
    assert clx.get_balance(ctx, account) == expected

    return account
