import typing

from stests.core.cache.utils import encache
from stests.core.domain import Account
from stests.core.domain import Transfer
from stests.core.domain import Deploy
from stests.core.domain import RunContext
from stests.core.domain import RunEvent



@encache
def set_run_account(ctx: RunContext, account: Account) -> typing.Tuple[typing.List[str], Account]:
    """Encaches domain object: Account.
    
    :param ctx: Generator run contextual information.
    :param account: Account domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return ["run-account"] + ctx.keypath + [str(account.index).zfill(6)], account
    

@encache
def set_run_context(ctx: RunContext) -> typing.Tuple[typing.List[str], RunContext]:
    """Encaches domain object: RunContext.
    
    :param ctx: Generator run contextual information.

    :returns: Keypath + domain object instance.

    """
    return ["run-context"] + ctx.keypath, ctx


@encache
def set_run_deploy(ctx: RunContext, deploy: Deploy) -> typing.Tuple[typing.List[str], Deploy]:
    """Encaches domain object: Deploy.
    
    :param ctx: Generator run contextual information.
    :param deploy: Deploy domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return ["run-deploy"] + ctx.keypath + [f"{str(deploy.ts_dispatched)}.{deploy.deploy_hash}"], deploy


@encache
def set_run_event(ctx: RunContext, evt: RunEvent) -> typing.Tuple[typing.List[str], RunEvent]:
    """Encaches domain object: RunEvent.
    
    :param ctx: Generator run contextual information.
    :param evt: RunEvent domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return ["run-event"] + ctx.keypath + [f"{str(evt.timestamp)}.{evt.event}"], evt


@encache
def set_run_transfer(ctx: RunContext, transfer: Transfer) -> typing.Tuple[typing.List[str], Transfer]:
    """Encaches domain object: Transfer.
    
    :param ctx: Generator run contextual information.
    :param transfer: Transfer domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return ["run-transfer"] + ctx.keypath + [transfer.asset.lower(), transfer.deploy_hash], transfer
