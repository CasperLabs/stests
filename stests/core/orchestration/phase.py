import dramatiq

from stests.core import cache
from stests.core import factory
from stests.core.logging import log_event
from stests.core.orchestration import predicates
from stests.core.orchestration.model import Workflow
from stests.core.orchestration.step import do_step
from stests.core.types.orchestration import ExecutionAspect
from stests.core.types.orchestration import ExecutionContext
from stests.core.types.orchestration import ExecutionStatus
from stests.events import EventType



# Queue to which messages will be dispatched.
_QUEUE = "orchestration.engine.phase"


@dramatiq.actor(queue_name=_QUEUE)
def do_phase(ctx: ExecutionContext):
    """Runs a workflow phase.
    
    :param ctx: Execution context information.
    
    """
    # Escape if unexecutable.
    if not _can_start(ctx):
        return

    # Update ctx.
    ctx.phase_index += 1
    ctx.step_index = 0

    # Update cache.
    cache.orchestration.set_context(ctx)
    cache.orchestration.set_info(factory.create_execution_info(
        ExecutionAspect.PHASE, ctx
        ))

    # Notify.
    log_event(EventType.WFLOW_PHASE_START, None, ctx)

    # Enqueue step.
    do_step.send(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def on_phase_end(ctx: ExecutionContext):
    """Ends a workflow phase.
    
    :param ctx: Execution context information.
    
    """
    # Set phase.
    phase = Workflow.get_phase_(ctx, ctx.phase_index)

    # Update cache.
    cache.orchestration.set_info_update(ctx, ExecutionAspect.PHASE, ExecutionStatus.COMPLETE)

    # Notify.
    log_event(EventType.WFLOW_PHASE_END, None, ctx)

    # Enqueue either end of workflow or next phase. 
    if phase.is_last:
        # JIT import to avoid circularity.
        from stests.core.orchestration.run import on_run_end
        on_run_end.send(ctx)
    else:
        do_phase.send(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def on_phase_error(ctx: ExecutionContext, err: str):
    """Ends a workflow phase in error.
    
    :param ctx: Execution context information.
    :param err: Execution error information.
    
    """
    # Update cache.
    cache.orchestration.set_info_update(ctx, ExecutionAspect.PHASE, ExecutionStatus.ERROR)

    # Notify.
    log_event(EventType.WFLOW_PHASE_ERROR, err, ctx)


def _can_start(ctx: ExecutionContext) -> bool:
    """Returns flag indicating whether a phase increment is valid.
    
    :param ctx: Execution context information.

    :returns: Flag indicating whether a phase increment is valid.

    """
    # False if workflow invalid.
    wflow, wflow_is_valid = predicates.is_valid_wflow(ctx)
    if not wflow_is_valid:
        return False

    # False if next phase not found.
    phase = wflow.get_phase(ctx.next_phase_index)
    if phase is None:
        log_event(EventType.WFLOW_PHASE_ABORT, None, ctx)
        return False

    # False if next phase locked.
    if not predicates.was_lock_acquired(ExecutionAspect.PHASE, ctx):
        return False
    
    # All tests passed, therefore return true.    
    return True