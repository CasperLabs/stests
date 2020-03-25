import typing

from stests.core import cache
from stests.core.orchestration import ExecutionAspect
from stests.core.orchestration import ExecutionLock
from stests.core.orchestration import ExecutionContext
from stests.core.utils import logger
from stests.orchestration import factory
from stests.orchestration.model import Workflow



def is_run_locked(ctx: ExecutionContext) -> bool:
    """Returns flag indicating whether a run is currently locked.
    
    :param ctx: Execution context information.

    :returns: Flag indicating whether a run is currently locked.

    """
    return cache.orchestration.get_lock_run(ctx) is not None


def is_valid_wflow(ctx: ExecutionContext) -> typing.Tuple[typing.Optional[Workflow], bool]:
    """Predicate determining whether the workflow to be executed is valid or not.
    
    """
    # False if workflow unregistered.
    try:
        wflow = Workflow.create(ctx)
    except ValueError:
        logger.log_warning(f"WFLOW :: {ctx.run_type} -> unregistered workflow")
        return None, False

    # False if workflow has no phases.
    if not wflow.phases:
        logger.log_warning(f"WFLOW :: {ctx.run_type} -> invalid workflow - has no associated phases")
        return None, False

    # False if a phase has no steps.
    for phase in wflow.phases:
        if not phase.steps:
            logger.log_warning(f"WFLOW :: {ctx.run_type} -> invalid workflow - a phase has no associated steps")
            return None, False

    # All tests passed, therefore return true.   
    return wflow, True


def was_lock_acquired(aspect: ExecutionAspect, ctx: ExecutionContext) -> bool:
    """Returns flag indicating whether an execution lock was acquired.
    
    :param aspect: Aspect of execution in scope.
    :param ctx: Execution context information.

    :returns: Flag indicating whether an execution lock was acquired

    """
    # Lock factory.
    def _create_lock(phase_index: int = None, step_index: int = None):
        return ExecutionLock(
            aspect=aspect,
            network=ctx.network,
            run_index=ctx.run_index,
            run_type=ctx.run_type,
            phase_index=phase_index,
            step_index=step_index,
            _type_key=None,
        )

    if aspect == ExecutionAspect.RUN:
        lock = _create_lock()
    elif aspect == ExecutionAspect.PHASE:
        lock = _create_lock(ctx.next_phase_index)
    elif aspect == ExecutionAspect.STEP:
        lock = _create_lock(ctx.phase_index, ctx.next_step_index)
    else:
        return False

    _, acquired = cache.orchestration.set_lock(aspect, lock)

    return acquired
