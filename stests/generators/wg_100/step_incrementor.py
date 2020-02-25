import inspect
import typing
from datetime import datetime as dt

import dramatiq

from stests.core import cache
from stests.core.utils import factory
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

MAP = {
    phase_1.do_fund_faucet: phase_1.do_fund_contract,
}


def increment(ctx: RunContext, step: RunStep):
    print(f"444 :: wg-100 :: increment")
    _increment_step(ctx, step, PIPELINE)


def _increment_step(ctx: RunContext, step: RunStep, pipeline: typing.Tuple[dramatiq.actor]):
    """Executes next step in workflow.
    
    """ 
    # Set next actor.
    next_actor = _get_next_actor(step, pipeline)

    # Set next step.
    next_step = factory.create_run_step(ctx, _get_actor_name(next_actor))
    cache.set_run_step(next_step)

    # Enqueue next actor.
    next_actor.send(ctx)


def _get_current_actor(step, pipeline):
    for actor in pipeline:
        if step.name == _get_actor_name(actor):
            return actor


def _get_next_actor(step, pipeline):
    for idx, actor in enumerate(pipeline):
        actor_name = _get_actor_name(actor)
        if step.name == actor_name:
            try:
                return pipeline[idx + 1]
            except IndexError:
                return None


def _get_actor_name(actor):
    fn = actor.fn
    m = inspect.getmodule(fn)

    return f"{m.__name__.split('.')[-1]}.{fn.__name__}"
