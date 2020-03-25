from stests.core.orchestration import *



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


def create_lock(aspect: ExecutionAspect, ctx: ExecutionContext, phase_index: int, step_index: int) -> ExecutionLock:
    """Factory: Returns an execution lock.
    
    :param aspect: Aspect of execution in scope.
    :param ctx: Execution context information.
    :param phase_index: Index of phase being locked.
    :param step_index: Index of step being locked.

    :returns: An execution lock.

    """
    return ExecutionLock(
        aspect=aspect,
        network=ctx.network,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        phase_index=phase_index,
        step_index=step_index,
        _type_key=None,
    )


def create_run_lock(ctx: ExecutionContext) -> ExecutionLock:
    """Factory: Returns an execution lock.
    
    :param ctx: Execution context information.

    :returns: An execution lock.

    """
    return ExecutionLock(
        aspect=ExecutionAspect.RUN,
        network=ctx.network,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        phase_index=None,
        step_index=None,
        _type_key=None,
    )


def create_phase_lock(ctx: ExecutionContext, phase_index: int) -> ExecutionLock:
    """Factory: Returns an execution lock.
    
    :param ctx: Execution context information.
    :param phase_index: Index of next execution phase.

    :returns: An execution lock.

    """
    return ExecutionLock(
        aspect=ExecutionAspect.PHASE,
        network=ctx.network,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        phase_index=phase_index,
        step_index=None,
        _type_key=None,
    )


def create_step_lock(ctx: ExecutionContext, step_index: int) -> ExecutionLock:
    """Factory: Returns an execution lock.
    
    :param ctx: Execution context information.
    :param step_index: Index of next execution step.

    :returns: An execution lock.

    """
    return ExecutionLock(
        aspect=ExecutionAspect.STEP,
        network=ctx.network,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        phase_index=ctx.phase_index,
        step_index=step_index,
        _type_key=None,
    )
