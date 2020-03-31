from datetime import datetime

from stests.core.orchestration import ExecutionAspect
from stests.core.orchestration import ExecutionContext
from stests.core.orchestration import ExecutionInfo
from stests.core.orchestration import ExecutionState
from stests.core.orchestration import ExecutionStatus


def create_info(aspect: ExecutionAspect, ctx: ExecutionContext) -> ExecutionInfo:
    """Returns a domain object instance: ExecutionInfo.

    :param aspect: Aspect of execution in scope.
    :param ctx: Execution context information.

    :returns: ExecutionInfo instance configured as per aspect.

    """
    info = ExecutionInfo(
        aspect=aspect,
        network=ctx.network,
        phase_index=None,
        run_index=ctx.run_index,
        run_index_parent=ctx.run_index_parent,
        run_type=ctx.run_type,
        status=ExecutionStatus.IN_PROGRESS,
        step_index=None,
        step_label=None,
        tp_duration=None,
        ts_start=datetime.now(),
        ts_end=None,
        _type_key=None,
    )

    if aspect == ExecutionAspect.PHASE:
        info.phase_index = ctx.phase_index
    elif aspect == ExecutionAspect.STEP:
        info.phase_index = ctx.phase_index
        info.step_index = ctx.step_index
        info.step_label = ctx.step_label

    return info


def create_state(aspect: ExecutionAspect, ctx: ExecutionContext, status: ExecutionStatus = None) -> ExecutionState:
    """Returns a domain object instance: ExecutionState.

    :param aspect: Aspect of execution in scope.
    :param ctx: Execution context information.
    :param status: Execution status.

    :returns: ExecutionState instance configured as per aspect.

    """
    state = ExecutionState(
        aspect=aspect,
        network=ctx.network,
        phase_index=None,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        status=ctx.status,
        step_index=None,
        step_label=None,
        _type_key=None
    )

    if aspect == ExecutionAspect.PHASE:
        state.phase_index = ctx.phase_index
    elif aspect == ExecutionAspect.STEP:
        state.phase_index = ctx.phase_index
        state.step_index = ctx.step_index
        state.step_label = ctx.step_label

    return state


