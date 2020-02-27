from stests.core import cache
from stests.core.domain import RunContext
from stests.core.domain import DeployStatus
from stests.core.domain import TransferStatus



def verify_fund_contract(ctx: RunContext, dhash: str):
    """Verifies that contract account is funded.
    
    """
    return _is_deploy_finalized(ctx, dhash) and _is_transfer_complete(ctx, dhash)


def verify_fund_faucet(ctx: RunContext, dhash: str):
    """Verifies that faucet account is funded.
    
    """
    return _is_deploy_finalized(ctx, dhash) and _is_transfer_complete(ctx, dhash)


def verify_fund_users(ctx: RunContext, dhash: str):
    """Verifies that user accounts are funded.
    
    """
    if not _is_deploy_finalized(ctx, dhash) or not _is_transfer_complete(ctx, dhash):
        return False
    
    return cache.get_step_deploy_count(ctx) == ctx.args.user_accounts


def _is_deploy_finalized(ctx, dhash):
    """Returns flag indicating whether a deploy is in a finalized state.
    
    """
    deploy = cache.get_run_deploy(dhash)

    return deploy and deploy.status == DeployStatus.FINALIZED


def _is_transfer_complete(ctx, dhash):
    """Returns flag indicating whether a transfer is in a finalized state.
    
    """
    transfer = cache.get_run_transfer(dhash)

    return transfer and transfer.status == TransferStatus.COMPLETE
