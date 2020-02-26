import inspect

import dramatiq

from stests.core.domain import RunContext
from stests.generators.wg_100 import phase_1
from stests.generators.wg_100 import phase_2



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
    actor.send(ctx)


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
