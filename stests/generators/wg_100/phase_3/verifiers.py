from stests.core import cache
from stests.core import clx
from stests.core.orchestration import ExecutionRunInfo
from stests.core.domain import DeployStatus
from stests.core.domain import Transfer
from stests.core.domain import TransferStatus



def verify_refund_step_1(ctx: ExecutionRunInfo, dhash: str):
    """Verifies a refund made during step 1.
    
    """
    _verify_deploy(ctx, dhash)
    _verify_refund(ctx, dhash)
    _verify_deploy_count(ctx, 1 + ctx.args.user_accounts)    


def verify_refund_step_2(ctx: ExecutionRunInfo, dhash: str):
    """Verifies a refund made during step 1.
    
    """
    _verify_deploy(ctx, dhash)
    _verify_refund(ctx, dhash)
    _verify_deploy_count(ctx, 1) 


def _verify_deploy(ctx: ExecutionRunInfo, dhash: str):
    """Verifies that a deploy is in a finalized state.
    
    """
    deploy = cache.get_run_deploy(dhash)
    assert deploy
    assert deploy.status == DeployStatus.FINALIZED


def _verify_deploy_count(ctx: ExecutionRunInfo, expected: int):
    """Verifies that a step's count of finalized deploys tallies.
    
    """
    assert cache.get_step_deploy_count(ctx) == expected


def _verify_refund(ctx: ExecutionRunInfo, dhash: str) -> Transfer:
    """Verifies that a refund between counter-parties completed.
    
    """
    refund = cache.get_run_transfer(dhash)
    assert refund
    assert refund.status == TransferStatus.COMPLETE
