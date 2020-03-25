import dramatiq

from stests.core import cache
from stests.core.orchestration import ExecutionAspect
from stests.core.orchestration import ExecutionStatus
from stests.core.orchestration import ExecutionContext
from stests.core.utils import logger
from stests.orchestration import factory
from stests.orchestration import predicates
from stests.orchestration.actors.phase import do_phase



# Queue to which messages will be dispatched.
_QUEUE = "orchestration"

# Default time period in milliseconds before next run loop is executed.
_DEFAULT_LOOP_INTERVAL_MS = 1000


@dramatiq.actor(queue_name=_QUEUE)
def do_run(ctx: ExecutionContext):
    """Runs a workflow.
    
    :param ctx: Execution context information.
    
    """
    # Escape if unexecutable.
    if not _can_run(ctx):
        return

    # Update ctx.
    ctx.status = ExecutionStatus.IN_PROGRESS

    # Set info/state.
    run_info = factory.create_info(ExecutionAspect.RUN, ctx)
    run_state = factory.create_state(ExecutionAspect.RUN, ctx)

    # Update cache.
    cache.flush_by_run(ctx)
    cache.orchestration.set_context(ctx)
    cache.orchestration.set_info(run_info)
    cache.orchestration.set_state(run_state)

    # Inform.
    logger.log(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} -> starts")

    # Run phase.
    do_phase.send(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def on_run_end(ctx: ExecutionContext):
    """Ends a workflow.
    
    :param ctx: Execution context information.
    
    """
    # Update ctx.
    ctx.status = ExecutionStatus.COMPLETE

    # Set info/state.
    run_state = factory.create_state(ExecutionAspect.RUN, ctx)

    # Update cache.
    cache.orchestration.set_context(ctx)
    cache.orchestration.set_state(run_state)
    cache.orchestration.update_info(ctx, ExecutionAspect.RUN, ExecutionStatus.COMPLETE)

    # Locks can now be flushed.
    cache.orchestration.flush_locks(ctx)    

    # Inform.
    logger.log(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} -> ends")

    # Loop.
    if ctx.loop_count != 0:
        _loop(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def on_run_error(ctx: ExecutionContext, err: str):
    """Ends a workflow phase in error.
    
    :param ctx: Execution context information.
    :param err: Execution error information.
    
    """
    # Update ctx.
    ctx.status = ExecutionStatus.ERROR

    # Set info/state.
    run_state = factory.create_state(ExecutionAspect.RUN, ctx)

    # Update cache.
    cache.orchestration.set_context(ctx)
    cache.orchestration.set_state(run_state)
    cache.orchestration.update_info(ctx, ExecutionAspect.RUN, ExecutionStatus.ERROR)

    # Inform.
    logger.log_error(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} -> unhandled error")
    logger.log_error(err)


def _can_run(ctx: ExecutionContext) -> bool:
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
        logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} -> invalid context (phase & step must be set to zero)")
        return False

    # False if locked.
    if not predicates.was_lock_acquired(ExecutionAspect.RUN, ctx):
        logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} -> unacquired lock")
        return False

    # All tests passed, therefore return true.    
    return True


def _loop(ctx):
    """Requeues execution if loop conditions are matched.
    
    """
    # Increment loop count & escape if all loops are complete.
    ctx.loop_index += 1
    if ctx.loop_count > 0 and ctx.loop_index > ctx.loop_count:
        return

    # Reset ctx fields.
    ctx.phase_index = 0
    ctx.run_index += 1
    ctx.status = ExecutionStatus.NULL
    ctx.step_index = 0

    # Set loop delay.
    loop_delay = ctx.loop_interval or _DEFAULT_LOOP_INTERVAL_MS

    # Enqueue next loop.
    do_run.send_with_options(args=(ctx, ), delay=loop_delay)
