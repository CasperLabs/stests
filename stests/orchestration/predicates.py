import typing

from stests.core import cache
from stests.core.orchestration import ExecutionContext
from stests.core.utils import logger
from stests.orchestration import factory
from stests.orchestration.model import Workflow



def can_start_run(ctx: ExecutionContext) -> bool:
    """Returns flag indicating whether a run increment is valid.
    
    :param ctx: Execution context information.

    :returns: Flag indicating whether a run increment is valid.

    """
    # False if workflow invalid.
    _, wflow_is_valid = _validate_wflow(ctx)
    if not wflow_is_valid:
        return False

    # False if phase/step are not initialised.
    if ctx.phase_index != 0 or ctx.step_index != 0:
        logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} -> invalid context (phase & step must be set to zero)")
        return False

    # False if locked.
    lock = factory.create_run_lock(ctx)
    _, acquired = cache.orchestration.lock_run(lock)
    if not acquired:
        logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} -> unacquired lock")
        return False

    # All tests passed, therefore return true.    
    return True


def can_start_phase(ctx: ExecutionContext) -> bool:
    """Returns flag indicating whether a phase increment is valid.
    
    :param ctx: Execution context information.

    :returns: Flag indicating whether a phase increment is valid.

    """
    # False if workflow invalid.
    wflow, wflow_is_valid = _validate_wflow(ctx)
    if not wflow_is_valid:
        return False

    # False if next phase not found.
    phase = wflow.get_phase(ctx.next_phase_index)
    if phase is None:
        logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.next_phase_index_label} -> invalid phase index")
        return False
    
    # False if next phase locked.
    lock = factory.create_phase_lock(ctx, ctx.next_phase_index)
    _, acquired = cache.orchestration.lock_phase(lock)
    if not acquired:
        logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.next_phase_index_label} -> unacquired phase lock")
        return False
    
    # All tests passed, therefore return true.    
    return True


def can_start_step(ctx: ExecutionContext) -> bool:
    """Returns flag indicating whether a step increment is valid.
    
    :param ctx: Execution context information.

    :returns: Flag indicating whether a step increment is valid.

    """
    # False if workflow invalid.
    wflow, wflow_is_valid = _validate_wflow(ctx)
    if not wflow_is_valid:
        return False

    # False if current phase not found.
    phase = wflow.get_phase(ctx.phase_index)
    if phase is None:
        logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} -> invalid phase index")
        return False
    
    # False if next step not found.
    step = phase.get_step(ctx.next_step_index)
    if step is None:
        logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.next_step_index_label} -> invalid step index")
        return False

    # False if next step locked - can happen when processing groups of messages.
    lock = factory.create_step_lock(ctx, ctx.next_step_index, step.label)
    _, acquired = cache.orchestration.lock_step(lock)
    if not acquired:
        return False
    
    # All tests passed, therefore return true.    
    return True


def _validate_wflow(ctx: ExecutionContext) -> typing.Tuple[typing.Optional[Workflow], bool]:
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
