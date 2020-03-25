import dramatiq

from stests.core import cache
from stests.core.orchestration import ExecutionAspect
from stests.core.orchestration import ExecutionStatus
from stests.core.orchestration import ExecutionContext
from stests.core.utils import logger
from stests.orchestration.model import Workflow
from stests.orchestration import factory
from stests.orchestration import predicates
from stests.orchestration.actors.step import do_step



# Queue to which messages will be dispatched.
_QUEUE = "orchestration"


@dramatiq.actor(queue_name=_QUEUE)
def do_phase(ctx: ExecutionContext):
    """Runs a workflow phase.
    
    :param ctx: Execution context information.
    
    """
    # Escape if unexecutable.
    if not predicates.can_start_phase(ctx):
        return

    # Update ctx.
    ctx.phase_index += 1
    ctx.step_index = 0

    # Set info/state.
    phase_info = factory.create_info(ExecutionAspect.PHASE, ctx)
    phase_state = factory.create_state(ExecutionAspect.PHASE, ctx, ExecutionStatus.IN_PROGRESS)

    # Update cache.
    cache.orchestration.set_context(ctx)
    cache.orchestration.set_info(phase_info)
    cache.orchestration.set_state(phase_state)

    # Inform.
    logger.log(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} -> starts")

    # Run step.
    do_step.send(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def on_phase_end(ctx: ExecutionContext):
    """Ends a workflow phase.
    
    :param ctx: Execution context information.
    
    """
    # Set phase.
    phase = Workflow.get_phase_(ctx, ctx.phase_index)

    # Set info/state.
    phase_state = factory.create_state(ExecutionAspect.PHASE, ctx, status=ExecutionStatus.COMPLETE)

    # Update cache.
    cache.orchestration.set_state(phase_state)
    cache.orchestration.update_info(ctx, ExecutionAspect.PHASE, ExecutionStatus.COMPLETE)

    # Inform.
    logger.log(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} -> ends")

    # Enqueue either end of workflow or next phase. 
    if phase.is_last:
        # JIT import to avoid circularity.
        from stests.orchestration.actors.run import on_run_end
        on_run_end.send(ctx)
    else:
        do_phase.send(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def on_phase_error(ctx: ExecutionContext, err: str):
    """Ends a workflow phase in error.
    
    :param ctx: Execution context information.
    :param err: Execution error information.
    
    """
    # Set info/state.
    phase_state = factory.create_state(ExecutionAspect.PHASE, ctx, status=ExecutionStatus.ERROR)

    # Update cache.
    cache.orchestration.set_state(phase_state)
    cache.orchestration.update_info(ctx, ExecutionAspect.PHASE, ExecutionStatus.ERROR)

    # Inform.
    logger.log_error(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} -> unhandled error")
    logger.log_error(err)
