import random
import typing

from stests.core.cache.locks import RunStepLock
from stests.core.cache.ops import StoreOperation
from stests.core.cache.ops_infra import get_network
from stests.core.cache.ops_infra import get_nodes
from stests.core.cache.partitions import StorePartition
from stests.core.cache.utils import cache_op
from stests.core.cache.utils import decache
from stests.core.cache.utils import do_incrby
from stests.core.cache.utils import encache
from stests.core.cache.utils import encache_lock
from stests.core.cache.utils import encache_singleton
from stests.core.cache.utils import pull_count
from stests.core.cache.utils import flushcache
from stests.core.domain import *
from stests.core.utils import factory



@cache_op(StorePartition.RUN, StoreOperation.FLUSH)
@flushcache
def flush_run(ctx: RunContext) -> typing.Generator:
    """Flushes previous run information.

    :param ctx: Generator run contextual information.

    :returns: A generator of keypaths to be flushed.
    
    """
    for collection in [
        "run-account",
        "run-context",
        "run-deploy",
        "run-event",
        "run-step",
        "run-step-deploy",
        "run-step-deploy-count",
        "run-step-lock",
        "run-transfer",
    ]:
        yield [
            collection,
            ctx.network,
            ctx.run_type,
            f"R-{str(ctx.run).zfill(3)}",
            "*"
        ]


@cache_op(StorePartition.RUN, StoreOperation.GET)
@decache
def get_account(account_id: AccountIdentifier) -> Account:
    """Decaches domain object: Account.

    :param account_id: An account identifier.

    :returns: A cached account.

    """
    run = account_id.run

    return [
        "run-account",
        run.network.name,
        run.type,
        f"R-{str(run.index).zfill(3)}",
        f"{str(account_id.index).zfill(6)}"
    ]


def get_run_account(ctx: RunContext, index: int) -> Account:
    """Decaches domain object: Account.
    
    :param ctx: Generator run contextual information.
    :param index: Run specific account index. 

    :returns: A cached account.

    """
    return get_account(factory.create_account_id(
        index,
        ctx.network,
        ctx.run,
        ctx.run_type
        ))


@cache_op(StorePartition.RUN, StoreOperation.GET)
@decache
def get_run_context(network, run_index, run_type) -> RunContext:
    """Decaches domain object: RunContext.
    
    :param ctx: Generator run contextual information.

    :returns: Cached run context information.

    """
    return [
        "run-context",
        network,
        run_type,
        f"R-{str(run_index).zfill(3)}"
    ]


def get_run_deploy(dhash: str) -> Deploy:
    """Decaches domain object: Deploy.
    
    :param dhash: A deploy hash.

    :returns: A run deploy.

    """    
    deploys = get_run_deploys(dhash)

    return deploys[-1] if deploys else None


@cache_op(StorePartition.RUN, StoreOperation.GET)
@decache
def get_run_deploys(dhash: str) -> typing.List[Deploy]:
    """Decaches collection of domain objects: Deploy.
    
    :param dhash: A deploy hash.

    :returns: List of matching deploys.

    """    
    return [f"run-deploy*{dhash}*"]


def get_run_network(ctx: RunContext) -> Network:
    """Decaches domain object: Network.
    
    :param ctx: Generator run contextual information.

    :returns: A registered network.

    """
    network_id = factory.create_network_id(ctx.network)

    return get_network(network_id)


def get_run_step(ctx: RunContext) -> RunStep:
    """Decaches domain object: RunStep.
    
    :param ctx: Generator run contextual information.

    :returns: Cached run step information.

    """
    steps = get_run_steps(ctx)
    steps = sorted(steps, key=lambda i: i.ts_start)

    return steps[-1] if steps else None


@cache_op(StorePartition.RUN, StoreOperation.GET)
@pull_count
def get_step_deploy_count(ctx: RunContext) -> int:
    """Reurns current count of run step deploys.

    :param ctx: Generator run contextual information.

    """
    return [
        "run-step-deploy-count",
        ctx.network,
        ctx.run_type,
        f"R-{str(ctx.run_index).zfill(3)}",
        ctx.run_step,
    ]


@cache_op(StorePartition.RUN, StoreOperation.GET)
@decache
def get_run_steps(ctx: RunContext) -> typing.List[RunStep]:
    """Decaches collection of domain objects: RunStep.

    :param ctx: Generator run contextual information.

    :returns: List of run steps.
    
    """
    return [
        "run-step",
        ctx.network,
        ctx.run_type,
        f"R-{str(ctx.run_index).zfill(3)}",
        "*"
        ]


def get_run_transfer(dhash: str) -> Transfer:
    """Decaches domain object: Transfer.
    
    :param dhash: A deploy hash.

    :returns: A run deploy.

    """    
    transfers = get_run_transfers(dhash)

    return transfers[-1] if transfers else None


@cache_op(StorePartition.RUN, StoreOperation.GET)
@decache
def get_run_transfers(dhash: str) -> typing.List[Transfer]:
    """Decaches collection of domain objects: Transfer.
    
    :param dhash: A deploy hash.

    :returns: Matched transfers.

    """    
    return [f"run-transfer*{dhash}*"]


@cache_op(StorePartition.RUN, StoreOperation.INCR)
@do_incrby
def increment_step_deploy_count(ctx: RunContext):
    """Increments (atomically) count of run step deploys.

    :param ctx: Generator run contextual information.

    """
    return [
        "run-step-deploy-count",
        ctx.network,
        ctx.run_type,
        f"R-{str(ctx.run_index).zfill(3)}",
        ctx.run_step,
    ]


@cache_op(StorePartition.RUN, StoreOperation.LOCK)
@encache_lock
def lock_run_step(lock: RunStepLock) -> typing.Tuple[typing.List[str], RunStepLock]:
    """Encaches a lock: RunStepLock.

    :param lock: Information to be locked.

    :returns: A cached account.

    """
    return [
        "run-step-lock",
        lock.network,
        lock.run_type,
        f"R-{str(lock.run_index).zfill(3)}",
        lock.step
    ], lock


@cache_op(StorePartition.RUN, StoreOperation.SET)
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


@cache_op(StorePartition.RUN, StoreOperation.SET)
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
        f"R-{str(ctx.run_index).zfill(3)}"
    ], ctx


@cache_op(StorePartition.RUN, StoreOperation.SET)
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
        f"{str(deploy.dispatch_ts.timestamp())}.{deploy.deploy_hash}"
    ], deploy


@cache_op(StorePartition.RUN, StoreOperation.SET)
@encache
def set_run_step(step: RunStep) -> typing.Tuple[typing.List[str], RunStep]:
    """Encaches domain object: RunStep.
    
    :param evt: RunStep domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        "run-step",
        step.network,
        step.run_type,
        f"R-{str(step.run).zfill(3)}",
        step.step
    ], step


@cache_op(StorePartition.RUN, StoreOperation.SET)
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
