from stests.core import cache
from stests.core import clx
from stests.core.domain import ExecutionRunInfo
from stests.core.domain import DeployStatus
from stests.core.domain import Transfer
from stests.core.domain import TransferStatus



def verify_fund_contract(ctx: ExecutionRunInfo, dhash: str):
    """Verifies that a contract account was funded.
    
    """
    _verify_deploy(ctx, dhash)
    transfer = _verify_transfer(ctx, dhash)
    _verify_account_balance(ctx, transfer.cp2_index, ctx.args.contract_initial_clx_balance)
    _verify_deploy_count(ctx, 1)    


def verify_fund_faucet(ctx: ExecutionRunInfo, dhash: str):
    """Verifies that a faucet account was funded.
    
    """
    _verify_deploy(ctx, dhash)
    transfer = _verify_transfer(ctx, dhash)
    _verify_account_balance(ctx, transfer.cp2_index, ctx.args.faucet_initial_clx_balance)
    _verify_deploy_count(ctx, 1)


def verify_fund_users(ctx: ExecutionRunInfo, dhash: str):
    """Verifies that user accounts are funded.
    
    """
    _verify_deploy(ctx, dhash)
    transfer = _verify_transfer(ctx, dhash)
    _verify_account_balance(ctx, transfer.cp2_index, ctx.args.user_initial_clx_balance)
    _verify_deploy_count(ctx, ctx.args.user_accounts)    


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


def _verify_transfer(ctx: ExecutionRunInfo, dhash: str) -> Transfer:
    """Verifies that a transfer between counter-parties completed.
    
    """
    transfer = cache.get_run_transfer(dhash)
    assert transfer
    assert transfer.status == TransferStatus.COMPLETE

    return transfer


def _verify_account_balance(ctx: ExecutionRunInfo, account_index: int, expected: int):
    """Verifies that an account balance is as per expectation.
    
    """
    account = cache.get_account_by_run(ctx, account_index)
    assert account
    assert clx.get_balance(ctx, account) == expected
