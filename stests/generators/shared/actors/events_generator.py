import dramatiq

from stests.core import cache
from stests.core.domain import RunContext
from stests.core.utils import factory



# Queue to which messages will be dispatched.
_QUEUE = f"global.events"


@dramatiq.actor(queue_name=f"{_QUEUE}.generator")
def do_persist_generator_event(ctx: RunContext, event_name: str):
    """Persists event information.
    
    """
    cache.set_run_event(ctx, factory.create_run_event(ctx, event_name))