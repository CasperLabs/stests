import dramatiq

from stests.core import cache
from stests.core import factory
from stests.core.logging import log_event
from stests.core.orchestration import predicates
from stests.core.orchestration.phase import do_phase
from stests.core.types.orchestration import ExecutionAspect
from stests.core.types.orchestration import ExecutionContext
from stests.core.types.orchestration import ExecutionMode
from stests.core.types.orchestration import ExecutionStatus
from stests.core.utils import encoder
from stests.events import EventType



# Queue to which messages will be dispatched.
_QUEUE = "orchestration.engine.run"

# Map: execution mode - > time period (in milliseconds) before next loop is executed.
_DEFAULT_LOOP_INTERVAL_MS = {
    ExecutionMode.SEQUENTIAL: int(2e3),
    ExecutionMode.PERIODIC: int(6e5),
}


@dramatiq.actor(queue_name=_QUEUE)
def do_run(ctx: ExecutionContext):
    """Runs a workflow.
    
    :param ctx: Execution context information.
    
    """
    # Escape if unexecutable.
    if not _can_start(ctx):
        return
    
    # Enqueue next run (when mode=PERIODIC).
    if ctx.execution_mode == ExecutionMode.PERIODIC:
        _loop(encoder.clone(ctx))

    # Update ctx.
    ctx.status = ExecutionStatus.IN_PROGRESS

    # Update cache.
    cache.orchestration.set_context(ctx)
    cache.orchestration.set_info(factory.create_execution_info(
        ExecutionAspect.RUN, ctx
        ))

    # Notify.
    log_event(EventType.WFLOW_RUN_START, None, ctx)

    # Enqueue phase.
    do_phase.send(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def on_run_end(ctx: ExecutionContext):
    """Ends a workflow.
    
    :param ctx: Execution context information.
    
    """
    # Update ctx.
    ctx.status = ExecutionStatus.COMPLETE

    # Update cache.
    cache.orchestration.set_context(ctx)
    cache.orchestration.set_info_update(ctx, ExecutionAspect.RUN, ExecutionStatus.COMPLETE)

    # Locks can now be deleted.
    cache.orchestration.delete_locks(ctx)   

    # Cache can now be pruned.
    if bool(ctx.prune_on_completion):
        cache.orchestration.prune_on_run_completion(ctx)   
        cache.state.prune_on_run_completion(ctx)

    # Notify.
    log_event(EventType.WFLOW_RUN_END, None, ctx)

    # Enqueue next run (when mode=SEQUENTIAL).
    if ctx.execution_mode == ExecutionMode.SEQUENTIAL:
        _loop(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def on_run_error(ctx: ExecutionContext, err: str):
    """Ends a workflow phase in error.
    
    :param ctx: Execution context information.
    :param err: Execution error information.
    
    """
    # Update ctx.
    ctx.status = ExecutionStatus.ERROR

    # Update cache.
    cache.orchestration.set_context(ctx)
    cache.orchestration.set_info_update(ctx, ExecutionAspect.RUN, ExecutionStatus.ERROR)

    # Notify.
    log_event(EventType.WFLOW_RUN_ERROR, err, ctx)


def _can_start(ctx: ExecutionContext) -> bool:
    """Returns flag indicating whether a run increment is valid.
    
    :param ctx: Execution context information.

    :returns: Flag indicating whether a run increment is valid.

    """
    # False if workflow invalid.
    _, wflow_is_valid = predicates.is_valid_wflow(ctx)
    if not wflow_is_valid:
        return False

    # False if phase/step are not initialised.
    if ctx.phase_index != 0 or ctx.step_index != 0:
        log_event(EventType.WFLOW_RUN_ABORT, None, ctx)
        return False

    # False if locked.
    if not predicates.was_lock_acquired(ExecutionAspect.RUN, ctx):
        return False

    # All tests passed, therefore return true.    
    return True


def _loop(ctx):
    """Requeues execution if loop conditions are matched.
    
    """
    # Escape if not looping.
    if ctx.loop_count == 0:
        return

    # Increment loop count & escape if all loops are complete.
    ctx.loop_index += 1
    if ctx.loop_count > 0 and ctx.loop_index > ctx.loop_count:
        return

    # Set unique run identifier.
    run_index = cache.orchestration.increment_generator_run_count(ctx.network, ctx.run_type)
    
    # Reset ctx fields.
    ctx.phase_index = 0
    ctx.run_index_parent = ctx.run_index
    ctx.run_index = run_index
    ctx.status = ExecutionStatus.NULL
    ctx.step_index = 0

    # Set loop delay.
    loop_delay = ctx.loop_interval_ms or _DEFAULT_LOOP_INTERVAL_MS[ctx.execution_mode]

    # Enqueue next loop.
    do_run.send_with_options(args=(ctx, ), delay=loop_delay)
