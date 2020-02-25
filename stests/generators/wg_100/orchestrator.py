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



# Queue to which message will be dispatched.
_QUEUE = f"generators.{constants.TYPE.lower()}"


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


@dramatiq.actor(queue_name=_QUEUE, actor_name="on_wg100_deploy_finalized")
def on_deploy_finalized(network, run_index, run_type, deploy_hash):
    """Callback: on_deploy_finalized.
    
    :param ctx: Generator run contextual information.

    """
    ctx = cache.get_run_context(network, run_index, run_type)
    _do_step_next(ctx, PIPELINE)


def _do_step_next(ctx: RunContext, pipeline: typing.Tuple[dramatiq.actor]):
    # Update current step.
    step = cache.get_run_step_current(ctx.network, ctx.run_index, ctx.run_type)    
    step.status = RunStepStatus.COMPLETE
    step.timestamp_end = dt.now().timestamp()
    cache.set_run_step(step)

    # Set next actor.
    next_actor = _get_next_actor(step, pipeline)

    # Set next step.
    next_step = factory.create_run_step(ctx, _get_actor_name(next_actor))
    cache.set_run_step(next_step)

    # Enqueue next actor.
    next_actor.send(ctx)


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
