from datetime import datetime as dt

import dramatiq

from stests.core import cache
from stests.core.utils import logger
from stests.core.domain import RunContext
from stests.core.domain import RunStepStatus
from stests.generators.wg_100 import step_incrementor as wg_100_incrementor
from stests.generators.wg_100 import step_verifier as wg_100_verifier



# Queue to which messages will be dispatched.
_QUEUE = "generators"

# Map: run type --> run step incrementor.
HANDLERS = {
    "WG-100": (wg_100_verifier, wg_100_incrementor),
}


@dramatiq.actor(queue_name=_QUEUE)
def correlate_finalized_deploy(ctx: RunContext, deploy_hash: str):   
    """Correlates a finalzied deploy with a workload generator correlation handler.
    
    :param network: Network name.
    :param run_index: Generator run index.
    :param run_type: Generator run type.
    :param deploy_hash: Hash of finalized deploy.

    """
    # Set handlers.
    try:
        verifier, incrementor = HANDLERS[ctx.run_type]
    except KeyError:
        logger.log_warning(f"{ctx.run_type} has no registered step verifier/incrementor")
        return

    # Set step.
    step = cache.get_run_step(ctx)   

    # Verify.
    if not verifier.verify(ctx, step):
        return

    # Mark current step as complete.
    step.status = RunStepStatus.COMPLETE
    step.timestamp_end = dt.now().timestamp()
    cache.set_run_step(step)

    # Increment.
    incrementor.increment(ctx, step)
