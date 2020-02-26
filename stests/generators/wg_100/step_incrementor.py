import inspect
import typing
from datetime import datetime as dt

import dramatiq

from stests.core import cache
from stests.core.cache import RunStepLock
from stests.core.utils import factory
from stests.core.utils import logger
from stests.core.domain import RunContext
from stests.core.domain import RunStep
from stests.core.domain import RunStepStatus
from stests.generators.wg_100 import constants
from stests.generators.wg_100 import phase_1
from stests.generators.wg_100 import phase_2
from stests.generators.wg_100 import step_verifier



PIPELINE = (
    phase_1.do_init_cache,
    phase_1.do_create_accounts,
    phase_1.do_fund_faucet,
    phase_1.do_fund_contract,
    phase_1.do_fund_users,
    phase_2.do_deploy_contract,
    phase_2.do_start_auction,
)


def increment(ctx: RunContext):
    """Performs a step increment by acquiring a step lock and dispatching a message to the step's actor.
    
    """
    actor = _get_next_actor(ctx.run_step, PIPELINE)
    if _can_step(ctx, actor):
        _set_step(ctx, actor)
        actor.send(ctx)


def _can_step(ctx, actor):
    """Predicate to determine if next step within a workflow can be executed or not.
    
    """
    step = _get_step(actor)
    lock = RunStepLock(
        network=ctx.network,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        step=step
    )
    _, acquired = cache.lock_run_step(lock)

    print(f"111 :: {ctx.run_type} :: {step} :: {acquired}")

    return acquired


def _set_step(ctx: RunContext, actor: dramatiq.Actor):
    """Executes next step in workflow.
    
    """ 
    step = _get_step(actor)
    cache.set_run_step(
        factory.create_run_step(ctx, step)
    )
    ctx.run_step = step
    cache.set_run_context(ctx)


def _get_step(actor: dramatiq.Actor) -> str:
    """Returns a queue name derived from module in which actor is declared.
    
    """
    m = inspect.getmodule(actor.fn)

    return f"{m.__name__.split('.')[-1]}.{actor.fn.__name__}"


def _get_next_actor(step, pipeline):
    """Derives next actor in pipeline.
    
    """
    for idx, actor in enumerate(pipeline):
        actor_name = _get_actor_name(actor)
        if step == actor_name:
            try:
                return pipeline[idx + 1]
            except IndexError:
                return None


def _get_actor_name(actor: dramatiq.Actor) -> str:
    """Gets name of actor so that it can be mapped to a step.
    
    """
    fn = actor.fn
    m = inspect.getmodule(fn)

    return f"{m.__name__.split('.')[-1]}.{fn.__name__}"


