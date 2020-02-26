from datetime import datetime as dt

import dramatiq

from stests.core import cache
from stests.core.utils import logger
from stests.core.domain import RunContext
from stests.core.domain import RunStepStatus
from stests.generators.wg_100 import incrementor as wg_100_incrementor
from stests.generators.wg_100 import verifier as wg_100_verifier



# Queue to which messages will be dispatched.
_QUEUE = "correlator"

# Map: run type --> run step incrementor.
HANDLERS = {
    "WG-100": (wg_100_verifier, wg_100_incrementor),
}


@dramatiq.actor(queue_name=_QUEUE)
def correlate_finalized_deploy(ctx: RunContext, deploy_hash: str):   
    """Correlates a finalzied deploy with a workload generator correlation handler.
    
    :param ctx: Generator run contextual information.
    :param deploy_hash: Hash of a finalized deploy.

    """
    # Set handlers.
    try:
        verifier, incrementor = HANDLERS[ctx.run_type]
    except KeyError:
        logger.log_warning(f"{ctx.run_type} has no registered step verifier/incrementor")
        return

    # Verify & increment.
    if verifier.verify(ctx, deploy_hash):
        _complete_step(ctx)
        incrementor.increment(ctx)


def _complete_step(ctx):
    """Returns step information for downstream correlation.
    
    """
    step = cache.get_run_step(ctx)
    step.status = RunStepStatus.COMPLETE
    step.timestamp_end = dt.now().timestamp()
    cache.set_run_step(step)