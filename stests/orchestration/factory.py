from stests.core.cache.locks import ExecutionRunLock
from stests.core.cache.locks import ExecutionPhaseLock
from stests.core.cache.locks import ExecutionStepLock

from stests.core.domain import ExecutionStatus
from stests.core.domain import RunContext
from stests.core.domain import RunContextState
from stests.core.domain import RunPhaseState
from stests.core.domain import RunStepState




def create_run_lock(ctx: RunContext) -> ExecutionRunLock:
    """Factory: Returns an execution lock.
    
    :param ctx: Execution context information.

    :returns: An execution lock.

    """
    return ExecutionRunLock(
        network=ctx.network,
        run_index=ctx.run_index,
        run_type=ctx.run_type
    )


def create_run_state(ctx: RunContext, status: ExecutionStatus) -> RunContextState:
    """Factory: Returns execution state information.
    
    :param ctx: Execution context information.
    :param status: Execution status.

    :returns: Execution state information.

    """
    return RunContextState(
        network=ctx.network,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        status=status
    )


def create_phase_lock(ctx: RunContext, phase_index: int) -> ExecutionRunLock:
    """Factory: Returns an execution lock.
    
    :param ctx: Execution context information.
    :param phase_index: Index of next execution phase.

    :returns: An execution lock.

    """
    return ExecutionPhaseLock(
        network=ctx.network,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        phase_index=phase_index
    )


def create_phase_state(ctx: RunContext, status: ExecutionStatus) -> RunPhaseState:
    """Factory: Returns execution state information.
    
    :param ctx: Execution context information.
    :param status: Execution status.

    :returns: Execution state information.

    """
    return RunPhaseState(
        network=ctx.network,
        phase_index=ctx.phase_index,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        status=status
    )


def create_step_lock(ctx: RunContext, step_index: int) -> ExecutionRunLock:
    """Factory: Returns an execution lock.
    
    :param ctx: Execution context information.
    :param step_index: Index of next execution step.

    :returns: An execution lock.

    """
    return ExecutionStepLock(
        network=ctx.network,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        phase_index=ctx.phase_index,
        step_index=step_index
    )
    

def create_step_state(ctx: RunContext, status: ExecutionStatus) -> RunStepState:
    """Factory: Returns execution state information.
    
    :param ctx: Execution context information.
    :param status: Execution status.

    :returns: Execution state information.

    """
    return RunStepState(
        network=ctx.network,
        phase_index=ctx.phase_index,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        status=status,
        step_index=ctx.step_index,
        step_label=ctx.step_label
    )
