import typing

from stests.core.domain import ExecutionStatus
from stests.core.domain import RunContext
from stests.core.domain import RunContextState
from stests.core.domain import RunPhaseState
from stests.core.domain import RunStepState



def create_state(
    ctx: RunContext,
    phase_index: int = None,
    step_index: int = None,
    status=ExecutionStatus.IN_PROGRESS
    ) -> typing.Union[RunContextState, RunPhaseState, RunStepState]:
    if ctx and phase_index and step_index:
        return RunStepState(
            network=ctx.network,
            phase_index=phase_index,
            run_index=ctx.run_index,
            run_type=ctx.run_type,
            status=status,
            step_index=step_index
        )

    elif ctx and phase_index:
        return RunPhaseState(
            network=ctx.network,
            phase_index=phase_index,
            run_index=ctx.run_index,
            run_type=ctx.run_type,
            status=status
        )

    elif ctx:
        return RunContextState(
            network=ctx.network,
            run_index=ctx.run_index,
            run_type=ctx.run_type,
            status=status
        )
