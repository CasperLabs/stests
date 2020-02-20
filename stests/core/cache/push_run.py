import typing

from stests.core.cache.utils import encache
from stests.core.domain import Account
from stests.core.domain import Transfer
from stests.core.domain import Deploy
from stests.core.domain import RunContext
from stests.core.domain import RunEvent



@encache
def set_run_account(account: Account) -> typing.Tuple[typing.List[str], Account]:
    """Encaches domain object: Account.
    
    :param account: Account domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        "run-account",
        account.network,
        account.run_type,
        f"R-{str(account.run).zfill(3)}",
        str(account.index).zfill(6)
    ], account    


@encache
def set_run_context(ctx: RunContext) -> typing.Tuple[typing.List[str], RunContext]:
    """Encaches domain object: RunContext.
    
    :param ctx: Generator run contextual information.

    :returns: Keypath + domain object instance.

    """
    return [
        "run-context",
        ctx.network,
        ctx.run_type,
        f"R-{str(ctx.run).zfill(3)}"
    ], ctx


@encache
def set_run_deploy(deploy: Deploy) -> typing.Tuple[typing.List[str], Deploy]:
    """Encaches domain object: Deploy.
    
    :param deploy: Deploy domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        "run-deploy",
        deploy.network,
        deploy.run_type,
        f"R-{str(deploy.run).zfill(3)}",
        f"{str(deploy.ts_dispatched)}.{deploy.deploy_hash}"
    ], deploy


@encache
def set_run_event(evt: RunEvent) -> typing.Tuple[typing.List[str], RunEvent]:
    """Encaches domain object: RunEvent.
    
    :param evt: RunEvent domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        "run-event",
        evt.network,
        evt.run_type,
        f"R-{str(evt.run).zfill(3)}",
        f"{str(evt.timestamp)}.{evt.event}"
    ], evt


@encache
def set_run_transfer(transfer: Transfer) -> typing.Tuple[typing.List[str], Transfer]:
    """Encaches domain object: Transfer.
    
    :param transfer: Transfer domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        "run-transfer",
        transfer.network,
        transfer.run_type,
        f"R-{str(transfer.run).zfill(3)}",
        transfer.asset.lower(),
        transfer.deploy_hash
    ], transfer
