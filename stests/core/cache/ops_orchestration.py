import random
import typing

import stests.core.cache.ops_infra as infra
from stests.core.cache.enums import StoreOperation
from stests.core.cache.enums import StorePartition
from stests.core.cache.utils import cache_op
from stests.core.domain import *
from stests.core.orchestration import *
from stests.core.utils import factory



@cache_op(StorePartition.ORCHESTRATION, StoreOperation.FLUSH)
def flush_by_network(network_id: NetworkIdentifier) -> typing.Generator:
    """Flushes network specific monitoring information.

    :param network_id: A network identifier.

    :returns: A generator of keypaths to be flushed.
    
    """
    yield ["context", network_id.name, "*"]
    yield ["lock", network_id.name, "*"]
    yield ["phase", network_id.name, "*"]
    yield ["step", network_id.name, "*"]
    yield ["step-deploy-count", network_id.name, "*"]
        

@cache_op(StorePartition.ORCHESTRATION, StoreOperation.FLUSH)
def flush_by_run(ctx: ExecutionRunInfo) -> typing.Generator:
    """Flushes previous run information.

    :param ctx: Generator run contextual information.

    :returns: A generator of keypaths to be flushed.
    
    """
    for collection in [
        "context",
        "phase",
        "step",
        "step-deploy-count",
    ]:
        yield [
            collection,
            ctx.network,
            ctx.run_type,
            f"R-{str(ctx.run_index).zfill(3)}",
            "*"
        ]


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.FLUSH)
def flush_locks(ctx: ExecutionRunInfo) -> typing.Generator:
    """Flushes previous run locks.

    :param ctx: Generator run contextual information.

    :returns: A generator of keypaths to be flushed.
    
    """
    yield [
        "lock",
        ctx.network,
        ctx.run_type,
        f"R-{str(ctx.run_index).zfill(3)}*",
    ]


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.GET)
def get_context(network: str, run_index: int, run_type: str) -> ExecutionRunInfo:
    """Decaches domain object: ExecutionRunInfo.
    
    :param network: Name of network being tested.
    :param run_index: Generator run index.
    :param run_type: Generator run type, e.g. wg-100.

    :returns: Cached run context information.

    """
    return [
        "context",
        network,
        run_type,
        f"R-{str(run_index).zfill(3)}"
    ]


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.GET)
def get_contexts(network: str, run_type: str) -> ExecutionRunInfo:
    """Decaches domain object: ExecutionRunInfo.
    
    :param ctx: Generator run contextual information.

    :returns: Cached run context information.

    """
    return [
        "context",
        network,
        run_type,
        "*"
    ]

def get_run_network(ctx: ExecutionRunInfo) -> Network:
    """Decaches domain object: Network.
    
    :param ctx: Generator run contextual information.

    :returns: A registered network.

    """
    network_id = factory.create_network_id(ctx.network)

    return infra.get_network(network_id)


def get_step(ctx: ExecutionRunInfo) -> ExecutionStepInfo:
    """Decaches domain object: ExecutionStepInfo.
    
    :param ctx: Generator run contextual information.

    :returns: Cached run step information.

    """
    steps = get_steps(ctx)
    steps = sorted(steps, key=lambda i: i.ts_start)

    return steps[-1] if steps else None


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.GET)
def get_steps(ctx: ExecutionRunInfo) -> typing.List[ExecutionStepInfo]:
    """Decaches collection of domain objects: ExecutionStepInfo.

    :param ctx: Generator run contextual information.

    :returns: List of run steps.
    
    """
    return [
        "step",
        ctx.network,
        ctx.run_type,
        ctx.run_index_label,
        "*"
        ]
        

@cache_op(StorePartition.ORCHESTRATION, StoreOperation.GET_COUNT)
def get_step_deploy_count(ctx: ExecutionRunInfo) -> int:
    """Reurns current count of run step deploys.

    :param ctx: Generator run contextual information.

    """
    keypath = [
        "step-deploy-count",
        ctx.network,
        ctx.run_type,
    ]
    if ctx.phase_index and ctx.step_index:
        keypath.append(f"{ctx.run_index_label}.{ctx.phase_index_label}.{ctx.step_index_label}")
    elif ctx.phase_index:
        keypath.append(f"{ctx.run_index_label}.{ctx.phase_index_label}")
    else:
        keypath.append(ctx.run_index_label)

    return keypath


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.INCR)
def increment_step_deploy_count(ctx: ExecutionRunInfo):
    """Increments (atomically) count of run step deploys.

    :param ctx: Generator run contextual information.

    """
    keypath = [
        "step-deploy-count",
        ctx.network,
        ctx.run_type,
    ]
    if ctx.phase_index and ctx.step_index:
        keypath.append(f"{ctx.run_index_label}.{ctx.phase_index_label}.{ctx.step_index_label}")
    elif ctx.phase_index:
        keypath.append(f"{ctx.run_index_label}.{ctx.phase_index_label}")
    else:
        keypath.append(ctx.run_index_label)

    return keypath


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.LOCK)
def lock_run(lock: ExecutionRunLock) -> typing.Tuple[typing.List[str], ExecutionRunLock]:
    """Encaches a lock: ExecutionRunLock.

    :param lock: Information to be locked.

    """
    return [
        "lock",
        lock.network,
        lock.run_type,
        lock.run_index_label
    ], lock


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.LOCK)
def lock_phase(lock: ExecutionPhaseLock) -> typing.Tuple[typing.List[str], ExecutionPhaseLock]:
    """Encaches a lock: ExecutionPhaseLock.

    :param lock: Information to be locked.

    """
    return [
        "lock",
        lock.network,
        lock.run_type,
        f"{lock.run_index_label}.{lock.phase_index_label}",
    ], lock


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.LOCK)
def lock_step(lock: ExecutionStepLock) -> typing.Tuple[typing.List[str], ExecutionStepLock]:
    """Encaches a lock: ExecutionStepLock.

    :param lock: Information to be locked.

    """
    return [
        "lock",
        lock.network,
        lock.run_type,
        f"{lock.run_index_label}.{lock.phase_index_label}.{lock.step_index_label}",
    ], lock


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.SET)
def set_state(
    state: typing.Union[ExecutionRunState, ExecutionPhaseState, ExecutionStepState]
    ) -> typing.Tuple[typing.List[str], typing.Union[ExecutionRunState, ExecutionPhaseState, ExecutionStepState]]:
    """Encaches domain object: ExecutionRunState.
    
    :param ctx: Generator run contextual information.

    :returns: Keypath + domain object instance.

    """
    keypath = [
            "state",
            state.network,
            state.run_type
        ]
    if isinstance(state, ExecutionRunState):
        keypath.append(state.run_index_label)
    elif isinstance(state, ExecutionPhaseState):
        keypath.append(f"{state.run_index_label}.{state.phase_index_label}")
    elif isinstance(state, ExecutionStepState):
        keypath.append(f"{state.run_index_label}.{state.phase_index_label}.{state.step_index_label}")
    else:
        raise TypeError()

    return keypath, state    


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.SET)
def set_run_context(ctx: ExecutionRunInfo) -> typing.Tuple[typing.List[str], ExecutionRunInfo]:
    """Encaches domain object: ExecutionRunInfo.
    
    :param ctx: Generator run contextual information.

    :returns: Keypath + domain object instance.

    """
    return [
        "context",
        ctx.network,
        ctx.run_type,
        f"R-{str(ctx.run_index).zfill(3)}"
    ], ctx


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.SET)
def set_run_step(step: ExecutionStepInfo) -> typing.Tuple[typing.List[str], ExecutionStepInfo]:
    """Encaches domain object: ExecutionStepInfo.
    
    :param evt: ExecutionStepInfo domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        "step",
        step.network,
        step.run_type,
        f"R-{str(step.run_index).zfill(3)}",
        step.step
    ], step

