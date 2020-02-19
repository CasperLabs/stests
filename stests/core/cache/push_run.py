from stests.core.cache.utils import encache
from stests.core.domain import Account
from stests.core.domain import Transfer
from stests.core.domain import Deploy
from stests.core.domain import RunContext
from stests.core.domain import RunEvent



@encache
def set_run_account(ctx: RunContext, account: Account):
    """Encaches domain object: Account.
    
    """
    return ["run-account"] + ctx.keypath + [str(account.index).zfill(6)], account
    

@encache
def set_run_context(ctx: RunContext):
    """Encaches domain object: RunContext.
    
    """
    return ["run-context"] + ctx.keypath, ctx


@encache
def set_run_deploy(ctx: RunContext, deploy: Deploy):
    """Encaches domain object: Deploy.
    
    """
    return ["run-deploy"] + ctx.keypath + [f"{str(deploy.ts_dispatched)}.{deploy.dhash}"], deploy


@encache
def set_run_event(ctx: RunContext, evt: RunEvent):
    """Encaches domain object: RunEvent.
    
    """
    return ["run-event"] + ctx.keypath + [f"{str(evt.timestamp)}.{evt.event}"], evt


@encache
def set_run_transfer(ctx: RunContext, transfer: Transfer):
    """Encaches domain object: Transfer.
    
    """
    return ["run-transfer"] + ctx.keypath + [transfer.asset.lower(), transfer.dhash], transfer
