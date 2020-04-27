import random
import typing

import stests.core.cache.ops_infra as infra
from stests.core.cache.model import StoreOperation
from stests.core.cache.model import StorePartition
from stests.core.cache.utils import cache_op
from stests.core.types.infra import NetworkIdentifier
from stests.core.types.orchestration import ExecutionAspect
from stests.core.types.orchestration import ExecutionContext
from stests.core.types.orchestration import ExecutionInfo
from stests.core.types.orchestration import ExecutionLock
from stests.core.types.orchestration import ExecutionStatus
from stests.core import factory


# Cache partition.
_PARTITION = StorePartition.ORCHESTRATION

# Cache collections.
COL_CONTEXT = "context"
COL_DEPLOY_COUNT = "deploy-count"
COL_GENERATOR_RUN_COUNT = "generator-run-count"
COL_INFO = "info"
COL_LOCK = "lock"
COL_STATE = "state"



@cache_op(_PARTITION, StoreOperation.FLUSH)
def flush_locks(ctx: ExecutionContext) -> typing.Generator:
    """Flushes previous run locks.

    :param ctx: Execution context information.

    :returns: A generator of keypaths to be flushed.
    
    """
    yield [
        ctx.network,
        ctx.run_type,
        ctx.label_run_index,
        COL_LOCK,
        "*",
    ]


@cache_op(_PARTITION, StoreOperation.GET)
def get_context(network: str, run_index: int, run_type: str) -> ExecutionContext:
    """Decaches domain object: ExecutionContext.
    
    :param network: Name of network being tested.
    :param run_index: Generator run index.
    :param run_type: Generator run type, e.g. wg-100.

    :returns: Cached run context information.

    """
    return [
        network,
        run_type,
        f"R-{str(run_index).zfill(3)}",
        COL_CONTEXT
    ]


@cache_op(_PARTITION, StoreOperation.GET)
def get_context_list(network_id: NetworkIdentifier, run_type: str) -> typing.List[ExecutionContext]:
    """Decaches domain object: ExecutionContext.
    
    :param network_id: Identifier of network being tested.
    :param run_type: Generator run type, e.g. wg-100.

    :returns: Cached run context information.

    """
    return [
        network_id.name,
        "WG-*" if run_type is None else run_type,
        "R-*",
        COL_CONTEXT,
    ]


@cache_op(_PARTITION, StoreOperation.GET_COUNT)
def get_deploy_count(ctx: ExecutionContext, aspect: ExecutionAspect) -> int:
    """Returns count of deploys within the scope of an execution aspect.

    :param ctx: Execution context information.
    :param aspect: Aspect of execution in scope.

    :returns: Count of deploys.

    """
    return _get_keypath_deploy_count(ctx, aspect)


@cache_op(_PARTITION, StoreOperation.GET_COUNTS)
def get_deploy_count_list(network_id: NetworkIdentifier, run_type: str = None, run_index: int = None) -> typing.List[str]:
    """Returns count of deploys within the scope of an execution aspect.

    :param network_id: Identifier of network being tested.
    :param run_type: Type of run that was executed.
    :param run_index: Index of a run.

    :returns: Count of deploys.

    """
    if run_type is None:
        path = [
            network_id.name,
            "*",
            "*",
            COL_DEPLOY_COUNT,
            "-"
        ]
    elif run_index:
        label_run_index = f"R-{str(run_index).zfill(3)}"
        path = [
            network_id.name,
            run_type,
            label_run_index,
            COL_DEPLOY_COUNT,
            "*"
        ]
    else:
        path = [
            network_id.name,
            run_type,
            "*",
            COL_DEPLOY_COUNT,
            "*",
        ]
    
    return path


@cache_op(_PARTITION, StoreOperation.GET)
def get_info(ctx: ExecutionContext, aspect: ExecutionAspect) -> ExecutionInfo:
    """Decaches domain object: ExecutionInfo.
    
    :param ctx: Execution information.

    :returns: Keypath to domain object instance.

    """
    path = [
        ctx.network,
        ctx.run_type,
        ctx.label_run_index,
        COL_INFO,
    ]

    if aspect == ExecutionAspect.RUN:
        path.append("-")
    elif aspect == ExecutionAspect.PHASE:
        path.append(ctx.label_phase_index)
    elif aspect == ExecutionAspect.STEP:
        path.append(f"{ctx.label_phase_index}.{ctx.label_step_index}")

    return path


@cache_op(_PARTITION, StoreOperation.GET)
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
        label_run_index = f"R-{str(run_index).zfill(3)}"
        return [
            network_id.name,
            run_type,
            label_run_index,
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


@cache_op(_PARTITION, StoreOperation.INCR)
def increment_deploy_count(ctx: ExecutionContext, aspect: ExecutionAspect = ExecutionAspect.STEP):
    """Increments (atomically) count of run step deploys.

    :param ctx: Execution context information.
    :param aspect: Aspect of execution in scope.

    """
    return _get_keypath_deploy_count(ctx, aspect), 1


@cache_op(_PARTITION, StoreOperation.INCR)
def increment_generator_run_count(network: str, generator_type: str) -> typing.List[str]:
    """Increments (atomically) count of generator runs.

    :param ctx: Execution context information.
    :param aspect: Aspect of execution in scope.

    """
    return [
        network,
        generator_type,
        COL_GENERATOR_RUN_COUNT
        ], 1


@cache_op(_PARTITION, StoreOperation.LOCK)
def set_lock(aspect: ExecutionAspect, lock: ExecutionLock) -> typing.Tuple[typing.List[str], ExecutionLock]:
    """Encaches a lock: ExecutionLock.

    :param aspect: Aspect of execution to be locked.
    :param lock: Information to be locked.

    """
    path = [
        lock.network,
        lock.run_type,
        lock.label_run_index,
        COL_LOCK,
    ]

    if aspect == ExecutionAspect.RUN:
        path.append("-")
    elif aspect == ExecutionAspect.PHASE:
        path.append(lock.label_phase_index)
    elif aspect == ExecutionAspect.STEP:
        path.append(f"{lock.label_phase_index}.{lock.label_step_index}")

    return path, lock


@cache_op(_PARTITION, StoreOperation.SET)
def set_context(ctx: ExecutionContext) -> typing.Tuple[typing.List[str], ExecutionContext]:
    """Encaches domain object: ExecutionContext.
    
    :param ctx: Execution context information.

    :returns: Keypath + domain object instance.

    """
    path = [
        ctx.network,
        ctx.run_type,
        ctx.label_run_index,
        COL_CONTEXT,
    ]

    return path, ctx


@cache_op(_PARTITION, StoreOperation.SET)
def set_info(info: ExecutionInfo) -> typing.Tuple[typing.List[str], ExecutionInfo]:
    """Encaches domain object: ExecutionInfo.
    
    :param info: ExecutionInfo domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    path = [
        info.network,
        info.run_type,
        info.label_run_index,
        COL_INFO,
    ]

    if info.phase_index and info.step_index:
        path.append(f"{info.label_phase_index}.{info.label_step_index}")
    elif info.phase_index:
        path.append(info.label_phase_index)
    else:
        path.append("-")

    return path, info


def set_info_update(ctx: ExecutionContext, aspect: ExecutionAspect, status: ExecutionStatus) -> ExecutionInfo:
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
        ctx.label_run_index,
        COL_DEPLOY_COUNT,
    ]

    if aspect == ExecutionAspect.RUN:
        path.append("-")
    elif aspect == ExecutionAspect.PHASE:
        path.append(ctx.label_phase_index)
    elif aspect == ExecutionAspect.STEP:
        path.append(f"{ctx.label_phase_index}.{ctx.label_step_index}")

    return path
