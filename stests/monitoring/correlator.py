import inspect
import typing
from datetime import datetime as dt

import dramatiq

from stests.core import cache
from stests.core.utils import logger
from stests.core.orchestration import ExecutionRunInfo
from stests.core.orchestration import ExecutionStatus
from stests.generators.wg_100 import pipeline as wg_100_pipeline


# Queue to which messages will be dispatched.
_QUEUE = "correlation"

# Map: run type --> run pipeline.
PIPELINES = {
    "WG-100": wg_100_pipeline,
}


@dramatiq.actor(queue_name=_QUEUE)
def correlate_finalized_deploy(ctx: ExecutionRunInfo, dhash: str):   
    """Correlates a finalzied deploy with a workload generator correlation handler.
    
    :param ctx: Generator run contextual information.
    :param dhash: Hash of a finalized deploy.

    """
    # Escape if no pipeline.
    try:
        pipeline = PIPELINES[ctx.run_type]
    except KeyError:
        logger.log_warning(f"Workload generator {ctx.run_type} has no registered pipeline")
        return
    
    # Escape if current step to actor mapping failed.
    actor = _get_actor(ctx, pipeline)
    if actor is None:
        logger.log_warning(f"Workload generator {ctx.run_type} {ctx.run_step} has no registered actor")
        return

    # Verify current step.
    if not _verify(ctx, pipeline, actor, dhash):
        return

    # Complete curent step.
    _complete_step(ctx)

    # Increment step.
    _increment(ctx, pipeline, actor)


def _complete_step(ctx):
    """Returns step information for downstream correlation.
    
    """
    step = cache.get_step(ctx)
    step.update_on_completion()
    cache.set_run_step(step)


def _complete_run(ctx):
    """Returns run information for downstream correlation.
    
    """
    _complete_step(ctx)
    # TODO: update run context status


def _verify(ctx: ExecutionRunInfo, pipeline, actor: dramatiq.Actor, dhash: str) -> bool:
    """Verifies that a step has completed prior to incrementation.
    
    """
    try:
        verifier = pipeline.VERIFIERS[actor]
    except KeyError:
        return True
    
    try:
        verifier(ctx, dhash)
    except AssertionError:
        logger.log_warning(f"{ctx.run_type} failed verification for step {ctx.run_step}")
        return False

    return True


def _increment(ctx: ExecutionRunInfo, pipeline, actor: dramatiq.Actor):
    """Increments a run step.
    
    """
    next_actor = _get_next_actor(ctx, pipeline, actor)
    if next_actor:
        next_actor.send(ctx)
    else:
        _complete_run(ctx)


def _get_actor(ctx: ExecutionRunInfo, pipeline) -> dramatiq.Actor:
    """Returns an actor from a pipeline bymatching it's name against a run step.
    
    """
    for actor in pipeline.PIPELINE:
        if ctx.run_step == _get_step_from_actor(actor):
            return actor


def _get_next_actor(ctx: ExecutionRunInfo, pipeline, actor: dramatiq.Actor) -> dramatiq.Actor:
    """Derives next actor in pipeline.
    
    """
    for idx, actor in enumerate(pipeline.PIPELINE):
        if ctx.run_step == _get_step_from_actor(actor):
            try:
                return pipeline.PIPELINE[idx + 1]
            except IndexError:
                return None


def _get_step_from_actor(actor: dramatiq.Actor) -> str:
    """Gets name of actor so that it can be mapped to a step.
    
    """
    fn = actor.fn
    m = inspect.getmodule(fn)

    return f"{m.__name__.split('.')[-1]}.{fn.__name__}"
