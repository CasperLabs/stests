import dramatiq

from stests.core import cache
from stests.core.domain import RunContext
from stests.core.utils import factory



# Queue to which messages will be dispatched.
_QUEUE = "generators.shared"


@dramatiq.actor(queue_name=_QUEUE)
def do_reset_cache(ctx: RunContext):   
    """Resets cache in preparation for a new run.
    
    :param ctx: Generator run contextual information.

    """
    # Flush previous cache data.
    cache.flush_run(ctx)

    # Cache.
    cache.set_run_context(ctx)

    # Chain.
    return ctx


