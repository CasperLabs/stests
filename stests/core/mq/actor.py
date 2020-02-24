import inspect
import functools

import dramatiq

from stests.core import cache
from stests.core.utils import factory



# Queue to which message will be dispatched.
_QUEUE = f"generators.wg-100"


def actorify(on_success=None):
    """Decorator to orthoganally convert a function into an actor.

    :param on_success: Continuation function upon execution success.

    :returns: Decorated function.
    
    """
    def decorator_actorify(func):

        @dramatiq.actor(queue_name=_QUEUE)
        @functools.wraps(func)
        def wrapper_actorify(*args, **kwargs):
            # Set actor name.
            actor_name = _get_actor_name(func)

            # Set context.
            ctx = args[0]
            
            # Set step.
            step = factory.create_run_step(ctx, actor_name)

            # Encache step.
            cache.set_run_step(step)

            # Invoke actor.
            result = func(*args, **kwargs)

            # Run groups.
            if isinstance(result, dramatiq.group):
                g = result
                if on_success:
                    g.add_completion_callback(on_success().message(ctx))
                g.run()

            # Enqueue continuation.
            elif on_success:
                on_success().send(ctx)

        return wrapper_actorify

    return decorator_actorify


def _get_actor_name(actor):
    m = inspect.getmodule(actor)

    return f"{m.__name__.split('.')[-1]}.{actor.__name__}"
