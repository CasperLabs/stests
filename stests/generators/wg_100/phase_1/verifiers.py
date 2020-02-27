from stests.core import cache
from stests.core.domain import RunContext
from stests.core.domain import DeployStatus
from stests.core.domain import TransferStatus



def verify_fund_contract(ctx: RunContext, dhash: str):
    """Verifies that contract account is funded.
    
    """
    _verify_deploy(ctx, dhash)
    _verify_deploy_count(ctx, 1)    
    _verify_transfer(ctx, dhash)


def verify_fund_faucet(ctx: RunContext, dhash: str):
    """Verifies that faucet account is funded.
    
    """
    _verify_deploy(ctx, dhash)
    _verify_deploy_count(ctx, 1)    
    _verify_transfer(ctx, dhash)


def verify_fund_users(ctx: RunContext, dhash: str):
    """Verifies that user accounts are funded.
    
    """
    _verify_deploy(ctx, dhash)
    _verify_deploy_count(ctx, ctx.args.user_accounts)    
    _verify_transfer(ctx, dhash)


def _verify_deploy(ctx: RunContext, dhash: str):
    """Returns flag indicating whether a deploy is in a finalized state.
    
    """
    deploy = cache.get_run_deploy(dhash)
    assert deploy and deploy.status == DeployStatus.FINALIZED


def _verify_deploy_count(ctx: RunContext, expected: int):
    """Returns flag indicating whether a step's count of finalized deploys tallies.
    
    """
    assert cache.get_step_deploy_count(ctx) == expected


def _verify_transfer(ctx: RunContext, dhash: str):
    """Returns flag indicating whether a transfer is in a finalized state.
    
    """
    transfer = cache.get_run_transfer(dhash)
    assert transfer and transfer.status == TransferStatus.COMPLETE

    # TODO: verify balance of cp2.
