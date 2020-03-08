import random
import typing

from stests.core.cache.locks import *
from stests.core.cache.enums import StoreOperation
from stests.core.cache.enums import StorePartition
from stests.core.cache.ops_infra import get_network
from stests.core.cache.ops_infra import get_nodes
from stests.core.cache.utils import cache_op
from stests.core.domain import *
from stests.core.utils import factory



@cache_op(StorePartition.CONTROL, StoreOperation.FLUSH)
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
        

@cache_op(StorePartition.CONTROL, StoreOperation.FLUSH)
def flush_by_run(ctx: RunContext) -> typing.Generator:
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


@cache_op(StorePartition.CONTROL, StoreOperation.FLUSH)
def flush_locks(ctx: RunContext) -> typing.Generator:
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


@cache_op(StorePartition.CONTROL, StoreOperation.GET)
def get_context(network: str, run_index: int, run_type: str) -> RunContext:
    """Decaches domain object: RunContext.
    
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


@cache_op(StorePartition.CONTROL, StoreOperation.GET)
def get_contexts(network: str, run_type: str) -> RunContext:
    """Decaches domain object: RunContext.
    
    :param ctx: Generator run contextual information.

    :returns: Cached run context information.

    """
    return [
        "context",
        network,
        run_type,
        "*"
    ]

def get_run_network(ctx: RunContext) -> Network:
    """Decaches domain object: Network.
    
    :param ctx: Generator run contextual information.

    :returns: A registered network.

    """
    network_id = factory.create_network_id(ctx.network)

    return get_network(network_id)


def get_step(ctx: RunContext) -> RunStep:
    """Decaches domain object: RunStep.
    
    :param ctx: Generator run contextual information.

    :returns: Cached run step information.

    """
    steps = get_steps(ctx)
    steps = sorted(steps, key=lambda i: i.ts_start)

    return steps[-1] if steps else None


@cache_op(StorePartition.CONTROL, StoreOperation.GET)
def get_steps(ctx: RunContext) -> typing.List[RunStep]:
    """Decaches collection of domain objects: RunStep.

    :param ctx: Generator run contextual information.

    :returns: List of run steps.
    
    """
    return [
        "step",
        ctx.network,
        ctx.run_type,
        f"R-{str(ctx.run_index).zfill(3)}",
        "*"
        ]
        

@cache_op(StorePartition.CONTROL, StoreOperation.GET_COUNT)
def get_step_deploy_count(ctx: RunContext) -> int:
    """Reurns current count of run step deploys.

    :param ctx: Generator run contextual information.

    """
    return [
        "step-deploy-count",
        ctx.network,
        ctx.run_type,
        f"R-{str(ctx.run_index).zfill(3)}",
        ctx.run_step,
    ]


@cache_op(StorePartition.CONTROL, StoreOperation.INCR)
def increment_step_deploy_count(ctx: RunContext):
    """Increments (atomically) count of run step deploys.

    :param ctx: Generator run contextual information.

    """
    return [
        "step-deploy-count",
        ctx.network,
        ctx.run_type,
        f"R-{str(ctx.run_index).zfill(3)}",
        ctx.run_step,
    ]


@cache_op(StorePartition.CONTROL, StoreOperation.LOCK)
def lock_run(lock: RunLock) -> typing.Tuple[typing.List[str], RunLock]:
    """Encaches a lock: RunLock.

    :param lock: Information to be locked.

    """
    return [
        "lock",
        lock.network,
        lock.run_type,
        lock.run_index_label
    ], lock


@cache_op(StorePartition.CONTROL, StoreOperation.LOCK)
def lock_phase(lock: RunPhaseLock) -> typing.Tuple[typing.List[str], RunPhaseLock]:
    """Encaches a lock: RunPhaseLock.

    :param lock: Information to be locked.

    """
    return [
        "lock",
        lock.network,
        lock.run_type,
        f"{lock.run_index_label}.{lock.phase_index_label}",
    ], lock


@cache_op(StorePartition.CONTROL, StoreOperation.LOCK)
def lock_step(lock: RunStepLock) -> typing.Tuple[typing.List[str], RunStepLock]:
    """Encaches a lock: RunStepLock.

    :param lock: Information to be locked.

    """
    return [
        "lock",
        lock.network,
        lock.run_type,
        f"{lock.run_index_label}.{lock.phase_index_label}.{lock.step_index_label}",
    ], lock


@cache_op(StorePartition.CONTROL, StoreOperation.SET)
def set_state(
    state: typing.Union[RunContextState, RunPhaseState, RunStepState]
    ) -> typing.Tuple[typing.List[str], typing.Union[RunContextState, RunPhaseState, RunStepState]]:
    """Encaches domain object: RunContextState.
    
    :param ctx: Generator run contextual information.

    :returns: Keypath + domain object instance.

    """
    keypath = [
            "state",
            state.network,
            state.run_type
        ]
    if isinstance(state, RunContextState):
        keypath.append(state.run_index_label)
    elif isinstance(state, RunPhaseState):
        keypath.append(f"{state.run_index_label}.{state.phase_index_label}")
    elif isinstance(state, RunStepState):
        keypath.append(f"{state.run_index_label}.{state.phase_index_label}.{state.step_index_label}")
    else:
        raise TypeError()

    return keypath, state    


@cache_op(StorePartition.CONTROL, StoreOperation.SET)
def set_run_context(ctx: RunContext) -> typing.Tuple[typing.List[str], RunContext]:
    """Encaches domain object: RunContext.
    
    :param ctx: Generator run contextual information.

    :returns: Keypath + domain object instance.

    """
    return [
        "context",
        ctx.network,
        ctx.run_type,
        f"R-{str(ctx.run_index).zfill(3)}"
    ], ctx


@cache_op(StorePartition.CONTROL, StoreOperation.SET)
def set_run_step(step: RunStep) -> typing.Tuple[typing.List[str], RunStep]:
    """Encaches domain object: RunStep.
    
    :param evt: RunStep domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        "step",
        step.network,
        step.run_type,
        f"R-{str(step.run_index).zfill(3)}",
        step.step
    ], step

