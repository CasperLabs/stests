import random
import time

import dramatiq

from stests.core import cache
from stests.core import factory
from stests.core.logging import log_event
from stests.core.mq.extensions import MessageGroup
from stests.core.orchestration.model import Workflow
from stests.core.orchestration.model import WorkflowStep
from stests.core.orchestration import predicates
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionAspect
from stests.core.types.orchestration import ExecutionContext
from stests.core.types.orchestration import ExecutionStatus
from stests.core.utils.exceptions import IgnoreableAssertionError
from stests.events import EventType




# Queue to which messages will be dispatched.
_QUEUE = "orchestration.engine.step"


@dramatiq.actor(queue_name=_QUEUE)
def do_step(ctx: ExecutionContext):
    """Runs a workflow step.
    
    :param ctx: Execution context information.
    
    """
    # Escape if unexecutable.
    if not _can_start(ctx):
        return

    # Set step.
    step = Workflow.get_phase_step(ctx, ctx.phase_index, ctx.step_index + 1)    
    if step is None:
        log_event(EventType.WFLOW_STEP_FAILURE, "invalid step", ctx)
        return

    # Update ctx.
    ctx.step_index += 1
    ctx.step_label = step.label

    # Update cache.
    cache.orchestration.set_context(ctx)
    cache.orchestration.set_info(factory.create_execution_info(ExecutionAspect.STEP, ctx))

    # Notify.
    log_event(EventType.WFLOW_STEP_START, None, ctx)

    # Execute.
    _execute(ctx, step)


@dramatiq.actor(queue_name=_QUEUE)
def do_step_verification(ctx: ExecutionContext):
    """Verifies a workflow step prior to signalling end.
    
    :param ctx: Execution context information.
    
    """
    # Set step.
    step = Workflow.get_phase_step(ctx, ctx.phase_index, ctx.step_index)
    if step is None:
        log_event(EventType.WFLOW_STEP_FAILURE, "invalid step", ctx)
        return

    # Verify step.
    if step.has_verifer and not step.has_verifer_for_deploy:
        try:
            step.verify(ctx)
        except AssertionError as err:
            log_event(EventType.WFLOW_STEP_FAILURE, "verification failed", ctx)
            return

    # Enqueue step end.
    on_step_end.send(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def on_step_end(ctx: ExecutionContext):
    """Ends a workflow step.
    
    :param ctx: Execution context information.
    
    """
    # Set step.
    step = Workflow.get_phase_step(ctx, ctx.phase_index, ctx.step_index)
    if step is None:
        log_event(EventType.WFLOW_STEP_FAILURE, "invalid step", ctx)
        return

    # Update cache.
    cache.orchestration.set_info_update(ctx, ExecutionAspect.STEP, ExecutionStatus.COMPLETE)

    # Notify.
    log_event(EventType.WFLOW_STEP_END, None, ctx)

    # Enqueue either end of phase or next step. 
    if step.is_last:
        # Note: JIT import to avoid circularity.
        from stests.core.orchestration.phase import on_phase_end
        on_phase_end.send(ctx)
    else:
        do_step.send(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def on_step_error(ctx: ExecutionContext, err: str):
    """Ends a workflow step in error.
    
    :param ctx: Execution context information.
    :param err: Execution error information.
    
    """
    # Update cache.
    cache.orchestration.set_info_update(ctx, ExecutionAspect.STEP, ExecutionStatus.ERROR)

    # Notify.
    log_event(EventType.WFLOW_STEP_ERROR, err, ctx)


@dramatiq.actor(queue_name=_QUEUE)
def on_step_deploy_finalized(ctx: ExecutionContext, node_id: NodeIdentifier, block_hash: str, deploy_hash: str):   
    """Processes a finalized deploy within the context of a step.
    
    :param ctx: Execution context information.
    :param node_id: Identifier of node that emitted block finalization event.
    :param block_hash: Hash of a finalized block.
    :param deploy_hash: Hash of a finalized deploy.

    """   
    # Set step - escape if not found.
    step = Workflow.get_phase_step(ctx, ctx.phase_index, ctx.step_index)
    if step is None:
        log_event(EventType.WFLOW_STEP_FAILURE, "invalid step", ctx)
        return

    # Escape if no deploy verifier.
    if not step.has_verifer_for_deploy:
        log_event(EventType.WFLOW_STEP_FAILURE, "deploy verifier undefined", ctx)
        return 

    # Verify deploy.
    try:
        step.verify_deploy(ctx, node_id, block_hash, deploy_hash)
    except AssertionError as err:
        log_event(EventType.WFLOW_STEP_FAILURE, f"deploy verification failed: {err} :: {deploy_hash}", ctx)
        return

    # Increment verified deploy counts.
    _, _, deploy_index = cache.orchestration.increment_deploy_counts(ctx)

    # Verify deploy batch is complete.
    try:
        step.verify_deploy_batch_is_complete(ctx, deploy_index)
    except:
        return

    # Verify step.
    if step.has_verifer:
        try:
            step.verify(ctx)
        except AssertionError as err:
            log_event(EventType.WFLOW_STEP_FAILURE, f"verification failed", ctx)
            return    

    # Step verification succeeded therefore signal step end.
    on_step_end.send(ctx)


def _can_start(ctx: ExecutionContext) -> bool:
    """Returns flag indicating whether a step increment is valid.
    
    :param ctx: Execution context information.

    :returns: Flag indicating whether a step increment is valid.

    """
    # False if workflow invalid.
    wflow, wflow_is_valid = predicates.is_valid_wflow(ctx)
    if not wflow_is_valid:
        return False

    # False if current phase not found.
    phase = wflow.get_phase(ctx.phase_index)
    if phase is None:
        log_event(EventType.WFLOW_STEP_ABORT, "invalid phase index", ctx)
        return False
    
    # False if next step not found.
    step = phase.get_step(ctx.next_step_index)
    if step is None:
        log_event(EventType.WFLOW_STEP_ABORT, "invalid step index", ctx)
        return False

    # False if next step locked - can happen when processing groups of messages.
    if not predicates.was_lock_acquired(ExecutionAspect.STEP, ctx):
        return False
    
    # All tests passed, therefore return true.    
    return True


def _execute(ctx: ExecutionContext, step: WorkflowStep):
    """Handles actual step execution.
    
    """
    # Execute - exceptions are trapped.
    step.execute(ctx)

    # Process errors.
    if step.error:
        on_step_error.send(ctx, str(step.error))

    # Exception if step result != None | tuple.
    elif step.result is not None and not isinstance(step.result, tuple):
        raise TypeError("Expecting either None or a tuple from a step function.")

    # Process result for async ops.
    elif step.is_async:
        _on_execute_async(ctx, step)

    # Process result for sync ops.
    else:
        _on_execute_sync(ctx, step)


def _on_execute_async(ctx: ExecutionContext, step: WorkflowStep):
    """Performs post asynchronous step work.
        
    """
    # Enqueue message.
    if isinstance(step.result, tuple) and len(step.result) == 2:
        _enqueue_message(ctx, step)

    # Enqueue message batch.
    elif isinstance(step.result, tuple) and len(step.result) == 3:
        _enqueue_message_batch(ctx, step)
    
    else:
        raise TypeError("Async steps must return either a single message or a batch of messages")


def _on_execute_sync(ctx: ExecutionContext, step: WorkflowStep):
    """Performs synchronous step work.
        
    """
    # If unit of work is complete then signal step end.
    if step.result is None:
        do_step_verification.send(ctx)

    # Enqueue message batch (with completion callback).
    elif isinstance(step.result, tuple) and len(step.result) == 3:
        _enqueue_message_batch(ctx, step)

    else:
        raise TypeError("Sync steps must return None or a batch of messages")


def _enqueue_message(ctx, step):
    """Enqueues a single message.
    
    """
    actor, args = step.result
    actor.send_with_options(args=args)


def _enqueue_message_batch(ctx, step):
    """Enqueues a message batch.
    
    """
    # Unpack step result.
    actor, count, args_factory = step.result

    # Yield args of messages to be enqueued.
    def message_factory():
        for args in args_factory():
            yield actor.message_with_options(args=args)

    # Instantiate a dramatiq group to batch message set.
    group = MessageGroup(message_factory())

    # When in sync mode we can signal end of step in a completion callback. 
    # In async mode the step end signal is determined post deploy finalisation event.
    if step.is_sync:
        group.add_completion_callback(do_step_verification.message(ctx))

    # Set window of dispatch.
    dispatch_window = None if not ctx.deploys_per_second else ctx.get_dispatch_window_ms(count)

    # Enqueue message batch.
    group.run(dispatch_window=dispatch_window)
