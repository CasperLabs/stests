from stests.core.domain import ExecutionStatus
from stests.core.domain import RunContext
from stests.core.domain import RunContextState
from stests.core.domain import RunPhaseState
from stests.core.domain import RunStepState



def create_state_run(ctx: RunContext, status: ExecutionStatus) -> RunContextState:
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


def create_state_phase(ctx: RunContext, status: ExecutionStatus) -> RunPhaseState:
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


def create_state_step(ctx: RunContext, status: ExecutionStatus) -> RunStepState:
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
        step_index=ctx.step_index
    )
