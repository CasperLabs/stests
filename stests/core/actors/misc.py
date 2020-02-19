import dramatiq

from stests.core import cache
from stests.core.domain import RunContext
from stests.core.utils import factory



# Queue to which messages will be dispatched.
_QUEUE = f"generators"


@dramatiq.actor(queue_name=_QUEUE)
def do_cache_context(ctx: RunContext):   
    """Pushes context to cache for downstream operations.
    
    """
    # Cache.
    cache.set_run(ctx)

    # Chain.
    return ctx
    

@dramatiq.actor(queue_name=_QUEUE)
def do_flush_cache(ctx: RunContext):   
    """Flushes cache in preparation for a new run.
    
    """
    # Flush previous cache data.
    cache.flush_run(ctx)

    # Chain.
    return ctx


@dramatiq.actor(queue_name=f"{_QUEUE}")
def do_persist_event(ctx: RunContext, event_name: str):
    """Persists event information.
    
    """
    cache.set_run_event(ctx, factory.create_run_event(ctx, event_name))
