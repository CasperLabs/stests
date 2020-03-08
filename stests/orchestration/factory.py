from stests.core.domain import ExecutionRunInfo
from stests.core.domain import ExecutionPhaseLock
from stests.core.domain import ExecutionPhaseState
from stests.core.domain import ExecutionRunLock
from stests.core.domain import ExecutionRunState
from stests.core.domain import ExecutionStatus
from stests.core.domain import ExecutionStepLock
from stests.core.domain import ExecutionStepState



def create_run_lock(ctx: ExecutionRunInfo) -> ExecutionRunLock:
    """Factory: Returns an execution lock.
    
    :param ctx: Execution context information.

    :returns: An execution lock.

    """
    return ExecutionRunLock(
        network=ctx.network,
        run_index=ctx.run_index,
        run_type=ctx.run_type
    )


def create_run_state(ctx: ExecutionRunInfo, status: ExecutionStatus) -> ExecutionRunState:
    """Factory: Returns execution state information.
    
    :param ctx: Execution context information.
    :param status: Execution status.

    :returns: Execution state information.

    """
    return ExecutionRunState(
        network=ctx.network,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        status=status
    )


def create_phase_lock(ctx: ExecutionRunInfo, phase_index: int) -> ExecutionRunLock:
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


def create_phase_state(ctx: ExecutionRunInfo, status: ExecutionStatus) -> ExecutionPhaseState:
    """Factory: Returns execution state information.
    
    :param ctx: Execution context information.
    :param status: Execution status.

    :returns: Execution state information.

    """
    return ExecutionPhaseState(
        network=ctx.network,
        phase_index=ctx.phase_index,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        status=status
    )


def create_step_lock(ctx: ExecutionRunInfo, step_index: int) -> ExecutionRunLock:
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
    

def create_step_state(ctx: ExecutionRunInfo, status: ExecutionStatus) -> ExecutionStepState:
    """Factory: Returns execution state information.
    
    :param ctx: Execution context information.
    :param status: Execution status.

    :returns: Execution state information.

    """
    return ExecutionStepState(
        network=ctx.network,
        phase_index=ctx.phase_index,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        status=status,
        step_index=ctx.step_index,
        step_label=ctx.step_label
    )
