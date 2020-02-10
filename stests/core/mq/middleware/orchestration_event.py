import datetime

import dramatiq

from stests.core import cache
from stests.core.domain import RunContext
from stests.core.utils import factory



# Queue to which message will be dispatched.
_QUEUE = f"global.orchestration"


@dramatiq.actor(queue_name=_QUEUE)
def do_persist_event(ctx, event_name):
    """Persists event information.
    
    """
    cache.set_run_event(factory.get_run_event(ctx, event_name))


class OrchestrationEventMiddleware(dramatiq.Middleware):
    """Middleware to automatically persist orchestration events.
    
    """
    def before_process_message(self, broker, message):
        """Called before a message is processed.

        :param broker: Message broker to which message was dispatched.
        :param message: A message being processed.

        """
        if isinstance(message.args, tuple) and len(message.args) > 0 and \
           _get_actor_name(message).startswith("on_"):
            args = message.args if isinstance(message.args[0], RunContext) else message.args[0]['args']
            if isinstance(args[0], RunContext):
                do_persist_event.send_with_options(
                    args=(args[0], _get_actor_name(message))
                    )        
            

def _get_actor_name(message):
    """Returns actor name by parsing incoming message.
    
    """
    return str(message).split('(')[0]

