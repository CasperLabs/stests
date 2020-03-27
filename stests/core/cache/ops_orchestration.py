import random
import typing

import stests.core.cache.ops_infra as infra
from stests.core.cache.enums import *
from stests.core.cache.utils import cache_op
from stests.core.domain import *
from stests.core.orchestration import *
from stests.core.utils import factory


# Cache collections.
COL_CONTEXT = "context"
COL_DEPLOY_COUNT = "deploy-count"
COL_GENERATOR_RUN_COUNT = "generator-run-count"
COL_INFO = "info"
COL_LOCK = "lock"
COL_STATE = "state"


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.FLUSH)
def flush_by_run(ctx: ExecutionContext) -> typing.Generator:
    """Flushes previous run information.

    :param ctx: Execution context information.

    :returns: A generator of keypaths to be flushed.
    
    """
    for collection in [
        COL_CONTEXT,
        COL_DEPLOY_COUNT,
        COL_INFO,
        COL_STATE,
    ]:
        yield [
            ctx.network,
            ctx.run_type,
            ctx.run_index_label,
            collection,
            "*"
        ]


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.FLUSH)
def flush_locks(ctx: ExecutionContext) -> typing.Generator:
    """Flushes previous run locks.

    :param ctx: Execution context information.

    :returns: A generator of keypaths to be flushed.
    
    """
    yield [
        ctx.network,
        ctx.run_type,
        ctx.run_index_label,
        COL_LOCK,
        "*",
    ]


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.GET)
def get_context(network: str, run_index: int, run_type: str) -> ExecutionContext:
    """Decaches domain object: ExecutionContext.
    
    :param network: Name of network being tested.
    :param run_index: Generator run index.
    :param run_type: Generator run type, e.g. wg-100.

    :returns: Cached run context information.

    """
    run_index_label = f"R-{str(run_index).zfill(3)}"

    return [
        network,
        run_type,
        run_index_label,
        COL_CONTEXT
    ]


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.GET)
def get_context_list(network_id: NetworkIdentifier, run_type: str) -> typing.List[ExecutionContext]:
    """Decaches domain object: ExecutionContext.
    
    :param network_id: Identifier of network being tested.
    :param run_type: Generator run type, e.g. wg-100.

    :returns: Cached run context information.

    """
    path = [
        network_id.name,
        "WG-*" if run_type is None else run_type,
        "R-*",
        COL_CONTEXT,
    ]

    return path


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.GET_COUNT)
def get_deploy_count(ctx: ExecutionContext, aspect: ExecutionAspect) -> int:
    """Returns count of deploys within the scope of an execution aspect.

    :param ctx: Execution context information.
    :param aspect: Aspect of execution in scope.

    :returns: Count of deploys.

    """
    return _get_keypath_deploy_count(ctx, aspect)


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.GET_COUNTS)
def get_deploy_count_list(network_id: NetworkIdentifier, run_type: str, run_index: int) -> typing.List[str]:
    """Returns count of deploys within the scope of an execution aspect.

    :param network_id: Identifier of network being tested.
    :param run_type: Type of run that was executed.
    :param run_index: Index of a run.

    :returns: Count of deploys.

    """
    run_index_label = f"R-{str(run_index).zfill(3)}"    

    path = [
        network_id.name,
        run_type,
        run_index_label,
        COL_DEPLOY_COUNT,
        "*"
    ]

    return path


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.GET)
def get_info(ctx: ExecutionContext, aspect: ExecutionAspect) -> ExecutionInfo:
    """Decaches domain object: ExecutionInfo.
    
    :param ctx: Execution information.

    :returns: Keypath to domain object instance.

    """
    path = [
        ctx.network,
        ctx.run_type,
        ctx.run_index_label,
        COL_INFO,
    ]

    if aspect == ExecutionAspect.RUN:
        path.append("-")
    elif aspect == ExecutionAspect.PHASE:
        path.append(ctx.phase_index_label)
    elif aspect == ExecutionAspect.STEP:
        path.append(f"{ctx.phase_index_label}.{ctx.step_index_label}")

    return path


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.GET)
def get_info_list(network_id: NetworkIdentifier, run_type: str, run_index: int = None) -> typing.List[ExecutionInfo]:
    """Decaches domain object: ExecutionInfo.
    
    :param network_id: Identifier of network being tested.
    :param run_type: Type of run that was executed.
    :param run_index: Index of a run.

    :returns: Keypath to domain object instance.

    """
    if not run_type:
        return [
            network_id.name,
            "*",
            COL_INFO,
            "*"
        ]
    elif run_index:
        run_index_label = f"R-{str(run_index).zfill(3)}"
        return [
            network_id.name,
            run_type,
            run_index_label,
            COL_INFO,
            "*"
        ]
    else:
        return [
            network_id.name,
            run_type,
            "*",
            COL_INFO,
            "*",
        ]


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.GET)
def get_lock_run(ctx: ExecutionContext) -> typing.Tuple[typing.List[str], ExecutionLock]:
    """Decaches domain object: ExecutionLock.
    
    :param ctx: Execution context information.

    :returns: Cached run step information.

    """
    return [
        ctx.network,
        ctx.run_type,
        ctx.run_index_label,
        COL_LOCK,
        "-"
    ]


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.INCR)
def increment_deploy_count(ctx: ExecutionContext, aspect: ExecutionAspect = ExecutionAspect.STEP):
    """Increments (atomically) count of run step deploys.

    :param ctx: Execution context information.
    :param aspect: Aspect of execution in scope.

    """
    return _get_keypath_deploy_count(ctx, aspect)


def increment_deploy_counts(ctx: ExecutionContext):
    """Increments (atomically) count of deploys.

    :param ctx: Execution context information.

    """
    increment_deploy_count(ctx, ExecutionAspect.RUN)
    increment_deploy_count(ctx, ExecutionAspect.PHASE)
    increment_deploy_count(ctx, ExecutionAspect.STEP)


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.INCR)
def increment_generator_run_count(network: str, generator_type: str) -> typing.List[str]:
    """Increments (atomically) count of generator runs.

    :param ctx: Execution context information.
    :param aspect: Aspect of execution in scope.

    """
    path = [
        network,
        generator_type,
        COL_GENERATOR_RUN_COUNT
        ]

    return path


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.LOCK)
def set_lock(aspect: ExecutionAspect, lock: ExecutionLock) -> typing.Tuple[typing.List[str], ExecutionLock]:
    """Encaches a lock: ExecutionLock.

    :param aspect: Aspect of execution to be locked.
    :param lock: Information to be locked.

    """
    path = [
        lock.network,
        lock.run_type,
        lock.run_index_label,
        COL_LOCK,
    ]

    if aspect == ExecutionAspect.RUN:
        path.append("-")
    elif aspect == ExecutionAspect.PHASE:
        path.append(lock.phase_index_label)
    elif aspect == ExecutionAspect.STEP:
        path.append(f"{lock.phase_index_label}.{lock.step_index_label}")

    return path, lock


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.SET)
def set_context(ctx: ExecutionContext) -> typing.Tuple[typing.List[str], ExecutionContext]:
    """Encaches domain object: ExecutionContext.
    
    :param ctx: Execution context information.

    :returns: Keypath + domain object instance.

    """
    path = [
        ctx.network,
        ctx.run_type,
        ctx.run_index_label,
        COL_CONTEXT,
    ]

    return path, ctx


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.SET)
def set_info(info: ExecutionInfo) -> typing.Tuple[typing.List[str], ExecutionInfo]:
    """Encaches domain object: ExecutionInfo.
    
    :param info: ExecutionInfo domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    path = [
        info.network,
        info.run_type,
        info.run_index_label,
        COL_INFO,
    ]

    if info.phase_index and info.step_index:
        path.append(f"{info.phase_index_label}.{info.step_index_label}")
    elif info.phase_index:
        path.append(info.phase_index_label)
    else:
        path.append("-")

    return path, info


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.SET)
def set_state(state: ExecutionState) -> typing.Tuple[typing.List[str], ExecutionState]:
    """Encaches domain object: ExecutionState.
    
    :param state: Execution state information.

    :returns: Keypath + domain object instance.

    """
    path = [
        state.network,
        state.run_type,
        state.run_index_label,
        COL_STATE,
    ]

    if state.aspect == ExecutionAspect.RUN:
        path.append("-")
    elif state.aspect == ExecutionAspect.PHASE:
        path.append(state.phase_index_label)
    elif state.aspect == ExecutionAspect.STEP:
        path.append(f"{state.phase_index_label}.{state.step_index_label}")

    return path, state


def update_info(ctx: ExecutionContext, aspect: ExecutionAspect, status: ExecutionStatus) -> ExecutionInfo:
    """Updates domain object: ExecutionContext.
    
    :param ctx: Execution context information.

    :returns: Keypath + domain object instance.

    """
    # Pull.
    info = get_info(ctx, aspect)

    # Update.
    info.end(status, None)

    # Recache.
    set_info(info)

    return info


def _get_keypath_deploy_count(ctx: ExecutionContext, aspect: ExecutionAspect) -> typing.List[str]:
    """Returns keypath used when working with a deploy count.
    
    """
    path = [
        ctx.network,
        ctx.run_type,
        ctx.run_index_label,
        COL_DEPLOY_COUNT,
    ]

    if aspect == ExecutionAspect.RUN:
        path.append("-")
    elif aspect == ExecutionAspect.PHASE:
        path.append(ctx.phase_index_label)
    elif aspect == ExecutionAspect.STEP:
        path.append(f"{ctx.phase_index_label}.{ctx.step_index_label}")

    return path
