import inspect
from datetime import datetime

import dramatiq

from stests.core import cache
from stests.core.orchestration import ExecutionAspect
from stests.core.orchestration import ExecutionStatus
from stests.core.orchestration import ExecutionContext
from stests.core.utils import logger

from stests.orchestration.model import Workflow
from stests.orchestration.model import WorkflowStep
from stests.orchestration import factory
from stests.orchestration import predicates



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
    if not predicates.can_start_run(ctx):
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
        do_run_loop(ctx)


def do_run_loop(ctx):
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


@dramatiq.actor(queue_name=_QUEUE)
def do_step(ctx: ExecutionContext):
    """Runs a workflow step.
    
    :param ctx: Execution context information.
    
    """
    # Escape if unexecutable.
    if not predicates.can_start_step(ctx):
        return

    # Set step.
    step = Workflow.get_phase_step(ctx, ctx.phase_index, ctx.step_index + 1)    

    # Update ctx.
    ctx.step_index += 1
    ctx.step_label = step.label

    # Set info/state.
    step_info = factory.create_info(ExecutionAspect.STEP, ctx)
    step_state = factory.create_state(ExecutionAspect.STEP, ctx, ExecutionStatus.IN_PROGRESS)

    # Update cache.
    cache.orchestration.set_context(ctx)
    cache.orchestration.set_info(step_info)
    cache.orchestration.set_state(step_state)

    # Inform.
    logger.log(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} :: {step.label} -> starts")

    # Execute.
    step.execute()

    # Process errors.
    if step.error:
        do_step_error.send(ctx, str(step.error))

    # Exception if step result != None | func.
    elif step.result is not None and not inspect.isfunction(step.result):
        raise TypeError("Expecting either none or a message factory from a step function.")

    # Process result for async ops.
    elif step.is_async:
        on_step_execute_async(ctx, step)

    # Process result for sync ops.
    else:
        on_step_execute_sync(ctx, step)


def on_step_execute_async(ctx: ExecutionContext, step: WorkflowStep):
    """Performs asynchronous step execution.
    
    :param ctx: Execution context information.
    :param step: Step related execution information.
    
    """
    # Message factories will be dispatched as a group, chain monitoring
    # subsequently signals to orchestrator that next step can be executed.
    if inspect.isfunction(step.result):
        message_factory = step.result()
        group = dramatiq.group(message_factory)
        group.run()

    logger.log(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} :: {step.label} -> listening for chain events")


def on_step_execute_sync(ctx: ExecutionContext, step: WorkflowStep):
    """Performs step execution.
    
    :param ctx: Execution context information.
    :param step: Step related execution information.
    
    """
    # Simply signal step end when unit of work executed.
    if step.result is None:
        do_step_end.send(ctx)

    # Dispatch message facctory as a group - note the completion callback.
    elif inspect.isfunction(step.result):
        message_factory = step.result()
        group = dramatiq.group(message_factory)
        group.add_completion_callback(do_step_end.message(ctx))
        group.run()


@dramatiq.actor(queue_name=_QUEUE)
def do_step_end(ctx: ExecutionContext):
    """Ends a workflow step.
    
    :param ctx: Execution context information.
    
    """
    # TODO: verify step execution before proceeding to next step.

    # Set step.
    step = Workflow.get_phase_step(ctx, ctx.phase_index, ctx.step_index)

    # Set info/state.
    step_state = factory.create_state(ExecutionAspect.STEP, ctx, ExecutionStatus.COMPLETE)

    # Update cache.
    cache.orchestration.set_state(step_state)
    cache.orchestration.update_info(ctx, ExecutionAspect.STEP, ExecutionStatus.COMPLETE)

    # Inform.
    logger.log(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} :: {step.label} -> end")

    # Enqueue either end of phase or next step. 
    if step.is_last:
        on_phase_end.send(ctx)
    else:
        do_step.send(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def do_step_error(ctx: ExecutionContext, err: str):
    """Ends a workflow step in error.
    
    :param ctx: Execution context information.
    :param err: Execution error information.
    
    """
    # Set info/state.
    step_state = factory.create_state(ExecutionAspect.STEP, ctx, ExecutionStatus.ERROR)

    # Update cache.
    cache.orchestration.set_state(step_state)
    cache.orchestration.update_info(ctx, ExecutionAspect.STEP, ExecutionStatus.ERROR)

    # Inform.
    logger.log_error(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} :: {ctx.step_label} -> unhandled error: {err}")


@dramatiq.actor(queue_name=_QUEUE)
def on_step_deploy_finalized(ctx: ExecutionContext, bhash: str, dhash: str):   
    """Processes a finalized deploy within the context of a step.
    
    :param ctx: Execution context information.
    :param bhash: Hash of a finalized block.
    :param dhash: Hash of a finalized deploy.

    """
    # Set step.
    step = Workflow.get_phase_step(ctx, ctx.phase_index, ctx.step_index)
    if step is None:
        logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} -> invalid step")

    # Verify step deploy:
    if not step.has_verifer_for_deploy:
        logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} -> deploy verifier undefined")
        return       
    else:
        try:
            step.verify_deploy(bhash, dhash)
        except AssertionError as err:
            logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} -> deploy verification failed: {err} :: {dhash}")
            return

    # Verify step:
    if not step.has_verifer:
        logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} -> step verifier undefined")
    else:
        try:
            step.verify()
        except AssertionError as err:
            logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} -> step verification failed")
            return       

    # Step verification succeeded therefore signal step end.
    do_step_end.send(ctx)
