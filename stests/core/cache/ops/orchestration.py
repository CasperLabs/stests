import random
import typing

from stests.core import factory
from stests.core.cache.model import CountIncrementKey
from stests.core.cache.model import Item
from stests.core.cache.model import ItemKey
from stests.core.cache.model import SearchKey
from stests.core.cache.model import StoreOperation
from stests.core.cache.model import StorePartition
from stests.core.cache.ops.utils import cache_op
from stests.core.types.infra import NetworkIdentifier
from stests.core.types.orchestration import ExecutionAspect
from stests.core.types.orchestration import ExecutionContext
from stests.core.types.orchestration import ExecutionInfo
from stests.core.types.orchestration import ExecutionLock
from stests.core.types.orchestration import ExecutionStatus
import stests.core.cache.ops.infra as infra



# Cache partition.
_PARTITION = StorePartition.ORCHESTRATION

# Cache collections.
COL_CONTEXT = "context"
COL_DEPLOY_COUNT = "deploy-count"
COL_GENERATOR_RUN_COUNT = "generator-run-count"
COL_INFO = "info"
COL_LOCK = "lock"

# Cache collection item expiration times.
EXPIRATION_COL_CONTEXT = 3600
EXPIRATION_COL_INFO = 3600


@cache_op(_PARTITION, StoreOperation.DELETE_MANY)
def delete_locks(ctx: ExecutionContext) -> SearchKey:
    """Flushes previous run locks.

    :param ctx: Execution context information.

    :returns: A generator of keypaths to be flushed.
    
    """
    return SearchKey(
        paths=[
            ctx.network,
            ctx.run_type,
            ctx.label_run_index,
            COL_LOCK,
        ]
    )


def prune_on_run_completion(ctx: ExecutionContext) -> SearchKey:
    """Deletes data cached during the course of a run.

    :param ctx: Execution context information.
    :returns: Cache search key under which all records will be deleted.

    """
    _delete_on_run_completion_1(ctx)
    _delete_on_run_completion_2(ctx)


@cache_op(_PARTITION, StoreOperation.DELETE_MANY)
def _delete_on_run_completion_1(ctx: ExecutionContext) -> SearchKey:
    """Deletes data cached during the course of a run.

    :param ctx: Execution context information.
    :returns: Cache search key under which all records will be deleted.

    """
    return SearchKey(
        paths=[
            ctx.network,
            ctx.run_type,
            ctx.label_run_index,
            COL_DEPLOY_COUNT,
            "P-"
        ]
    )


@cache_op(_PARTITION, StoreOperation.DELETE_MANY)
def _delete_on_run_completion_2(ctx: ExecutionContext) -> SearchKey:
    """Deletes data cached during the course of a run.

    :param ctx: Execution context information.
    :returns: Cache search key under which all records will be deleted.

    """
    return SearchKey(
        paths=[
            ctx.network,
            ctx.run_type,
            ctx.label_run_index,
            COL_INFO,
            "P-"
        ]
    )


@cache_op(_PARTITION, StoreOperation.GET_ONE)
def get_context(network: str, run_index: int, run_type: str) -> ItemKey:
    """Decaches domain object: ExecutionContext.
    
    :param network: Name of network being tested.
    :param run_index: Generator run index.
    :param run_type: Generator run type, e.g. wg-100.

    :returns: Cached run context information.

    """
    return ItemKey(
        paths=[
            network,
            run_type,
            f"R-{str(run_index).zfill(3)}",
        ],
        names=[
            COL_CONTEXT,
        ],
    )


@cache_op(_PARTITION, StoreOperation.GET_MANY)
def get_context_list(network_id: NetworkIdentifier, run_type: str) -> SearchKey:
    """Decaches domain object: ExecutionContext.
    
    :param network_id: Identifier of network being tested.
    :param run_type: Generator run type, e.g. wg-100.

    :returns: Cached run context information.

    """
    return SearchKey(
        paths=[
            network_id.name,
            "WG-*" if run_type is None else run_type,
            "R-*",
            COL_CONTEXT,
        ]
    )


@cache_op(_PARTITION, StoreOperation.GET_COUNTER_ONE)
def get_deploy_count(ctx: ExecutionContext, aspect: ExecutionAspect) -> ItemKey:
    """Returns count of deploys within the scope of an execution aspect.

    :param ctx: Execution context information.
    :param aspect: Aspect of execution in scope.

    :returns: Count of deploys.

    """
    if aspect == ExecutionAspect.RUN:
        names = ["-"]
    elif aspect == ExecutionAspect.PHASE:
        names = [ctx.label_phase_index]
    elif aspect == ExecutionAspect.STEP:
        names = [ctx.label_phase_index, ctx.label_step_index]

    return ItemKey(
        paths=[
            ctx.network,
            ctx.run_type,
            ctx.label_run_index,
            COL_DEPLOY_COUNT,
        ],
        names=names,
    )


@cache_op(_PARTITION, StoreOperation.GET_COUNTER_MANY)
def get_deploy_count_list(network_id: NetworkIdentifier, run_type: str = None, run_index: int = None) -> typing.List[str]:
    """Returns count of deploys within the scope of an execution aspect.

    :param network_id: Identifier of network being tested.
    :param run_type: Type of run that was executed.
    :param run_index: Index of a run.

    :returns: Count of deploys.

    """
    if run_type is None:
        return SearchKey(
            paths=[
                network_id.name,
                "*",
                "*",
                COL_DEPLOY_COUNT,
                "-",                
            ],
        )

    elif run_index:
        return SearchKey(
            paths=[
                network_id.name,
                run_type,
                f"R-{str(run_index).zfill(3)}",
                COL_DEPLOY_COUNT,
            ]
        )

    else:
        return SearchKey(
            paths=[
                network_id.name,
                run_type,
                "*",
                COL_DEPLOY_COUNT,
            ]
        )


@cache_op(_PARTITION, StoreOperation.GET_ONE)
def get_info(ctx: ExecutionContext, aspect: ExecutionAspect) -> ItemKey:
    """Decaches domain object: ExecutionInfo.
    
    :param ctx: Execution information.

    :returns: Keypath to domain object instance.

    """
    if aspect == ExecutionAspect.RUN:
        names = ["-"]
    elif aspect == ExecutionAspect.PHASE:
        names = [ctx.label_phase_index]
    elif aspect == ExecutionAspect.STEP:
        names = [ctx.label_phase_index, ctx.label_step_index]

    return ItemKey(
        paths=[
            ctx.network,
            ctx.run_type,
            ctx.label_run_index,
            COL_INFO,
        ],
        names=names,
    )


@cache_op(_PARTITION, StoreOperation.GET_MANY)
def get_info_list(network_id: NetworkIdentifier, run_type: str, run_index: int = None) -> SearchKey:
    """Decaches domain object: ExecutionInfo.
    
    :param network_id: Identifier of network being tested.
    :param run_type: Type of run that was executed.
    :param run_index: Index of a run.

    :returns: Keypath to domain object instance.

    """
    if not run_type:
        return SearchKey(
            paths=[
                network_id.name,
                "*",
                COL_INFO,
            ]
        )
    elif run_index:
        return SearchKey(
            paths=[
                network_id.name,
                run_type,
                f"R-{str(run_index).zfill(3)}",
                COL_INFO,
            ]
        )
    else:
        return SearchKey(
            paths=[
                network_id.name,
                run_type,
                "*",
                COL_INFO,
            ]
        )


@cache_op(_PARTITION, StoreOperation.COUNTER_INCR)
def increment_deploy_count(
    ctx: ExecutionContext,
    aspect: ExecutionAspect = ExecutionAspect.STEP,
    amount: int = 1,
    ) -> CountIncrementKey:
    """Increments (atomically) count of run step deploys.

    :param ctx: Execution context information.
    :param aspect: Aspect of execution in scope.
    :param amount: Amount by which to increment counter.

    """
    if aspect == ExecutionAspect.RUN:
        names = ["-"]
    elif aspect == ExecutionAspect.PHASE:
        names = [ctx.label_phase_index]
    elif aspect == ExecutionAspect.STEP:
        names = [ctx.label_phase_index, ctx.label_step_index]

    return CountIncrementKey(
        paths=[
            ctx.network,
            ctx.run_type,
            ctx.label_run_index,
            COL_DEPLOY_COUNT,
        ],
        names=names,
        amount=amount,
    )


def increment_deploy_counts(ctx: ExecutionContext, amount: int = 1) -> int:
    """Increments (atomically) count of run deploys.

    :param ctx: Execution context information.

    """
    # TODO: increment as a batch.
    return (
        increment_deploy_count(ctx, ExecutionAspect.RUN, amount),
        increment_deploy_count(ctx, ExecutionAspect.PHASE, amount),
        increment_deploy_count(ctx, ExecutionAspect.STEP, amount)
    )


@cache_op(_PARTITION, StoreOperation.COUNTER_INCR)
def increment_generator_run_count(network: str, generator_type: str) -> CountIncrementKey:
    """Increments (atomically) count of generator runs.

    :param ctx: Execution context information.
    :param aspect: Aspect of execution in scope.

    """
    return CountIncrementKey(
        paths=[
            network,
            generator_type,
        ],
        names=[
            COL_GENERATOR_RUN_COUNT
        ],
        amount=1
    )


@cache_op(_PARTITION, StoreOperation.SET_ONE_SINGLETON)
def set_lock(aspect: ExecutionAspect, lock: ExecutionLock) -> Item:
    """Encaches a lock: ExecutionLock.

    :param aspect: Aspect of execution to be locked.
    :param lock: Information to be locked.

    """
    if aspect == ExecutionAspect.RUN:
        names = ["-"]
    elif aspect == ExecutionAspect.PHASE:
        names = [lock.label_phase_index]
    elif aspect == ExecutionAspect.STEP:
        names = [lock.label_phase_index, lock.label_step_index]

    return Item(
        data=lock,
        item_key=ItemKey(
            paths=[
                lock.network,
                lock.run_type,
                lock.label_run_index,
                COL_LOCK,
            ],
            names=names,
        ),
    )


@cache_op(_PARTITION, StoreOperation.SET_ONE)
def set_context(ctx: ExecutionContext) -> Item:
    """Encaches domain object: ExecutionContext.
    
    :param ctx: Execution context information.

    :returns: Keypath + domain object instance.

    """
    return Item(
        data=ctx,
        item_key=ItemKey(
            paths=[
                ctx.network,
                ctx.run_type,
                ctx.label_run_index,
            ],
            names=[
                COL_CONTEXT,
            ],
        ),
        expiration=EXPIRATION_COL_CONTEXT
    )


@cache_op(_PARTITION, StoreOperation.SET_ONE)
def set_info(info: ExecutionInfo) -> Item:
    """Encaches domain object: ExecutionInfo.
    
    :param info: ExecutionInfo domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    if info.phase_index and info.step_index:
        names = [info.label_phase_index, info.label_step_index]
    elif info.phase_index:
        names = [info.label_phase_index]
    else:
        names = ["-"]

    return Item(
        data=info,
        item_key=ItemKey(
            paths=[
                info.network,
                info.run_type,
                info.label_run_index,
                COL_INFO,
            ],
            names=names,
        ),
        expiration=EXPIRATION_COL_INFO
    )    


def set_info_update(ctx: ExecutionContext, aspect: ExecutionAspect, status: ExecutionStatus):
    """Updates domain object: ExecutionContext.
    
    :param ctx: Execution context information.
    :param aspect: Aspect of execution in scope.
    :param status: New execution status.

    """
    info = get_info(ctx, aspect)
    info.end(status, None)
    set_info(info)
