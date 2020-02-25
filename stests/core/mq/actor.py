import inspect
import functools
import typing
from datetime import datetime as dt

import dramatiq

from stests.core import cache
from stests.core.utils import factory
from stests.core.domain import RunStepStatus



# Queue to which message will be dispatched.
_QUEUE = f"generators.wg-100"


def actorify(on_success=None, is_substep=False):
    """Decorator to orthoganally convert a function into an actor.

    :param on_success: Continuation function upon execution success.
    :param is_substep: Flag indicating whether actor is a sub-step or not.

    :returns: Decorated function.
    
    """
    def decorator_actorify(func):

        @dramatiq.actor(queue_name=_get_queue_name(func))
        @functools.wraps(func)
        def wrapper_actorify(*args, **kwargs):
            # Set context.
            ctx = args[0]
            
            # Encache step.
            step = _get_step(ctx, func) if not is_substep else None

            # Invoke actor.
            result = func(*args, **kwargs)

            # Message factories --> dramatiq.group.
            if inspect.isfunction(result):
                result = dramatiq.group(result())

            # Update step.
            if step and on_success:
                _set_step(step)

            # Groups.
            if isinstance(result, dramatiq.group):
                if on_success:
                    result.add_completion_callback(on_success().message(ctx))
                result.run()

            # Continuation.
            elif on_success:
                on_success().send(ctx)

        return wrapper_actorify

    return decorator_actorify


def _get_step(ctx, actor):
    """Returns step information for downstream correlation.
    
    """
    step_name = _get_step_name(actor)
    step = factory.create_run_step(ctx, step_name)
    cache.set_run_step(step)

    return step


def _get_step_name(actor):
    """Returns a queue name derived from module in which actor is declared.
    
    """
    m = inspect.getmodule(actor)

    return f"{m.__name__.split('.')[-1]}.{actor.__name__}"


def _get_queue_name(actor):
    """Returns a queue name derived from module in which actor is declared.
    
    """
    m = inspect.getmodule(actor)

    return f"{m.__name__.split('.')[-2]}".replace('_', "-")


def _set_step(step):
    """Returns step information for downstream correlation.
    
    """
    step.status = RunStepStatus.COMPLETE
    step.timestamp_end = dt.now().timestamp()
    cache.set_run_step(step)
