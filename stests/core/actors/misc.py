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


@dramatiq.actor(queue_name=f"{_QUEUE}")
def on_run_event(ctx: RunContext, event_name: str):
    """Event: raised whenever a run event is fired.
    
    :param ctx: Generator run contextual information.
    :param event_name: Name of run event.

    """
    # Encache.
    cache.set_run_event(factory.create_run_event(ctx, event_name))
