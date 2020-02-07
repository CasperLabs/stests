import datetime

import dramatiq

from stests.core import cache
from stests.core.types import GeneratorRun
from stests.core.types.generator_run import GeneratorRunStatus
from stests.core.utils import logger as _logger



# Queue to which message will be dispatched.
_QUEUE = f"global.orchestration"



@dramatiq.actor(queue_name=_QUEUE)
def do_update_status(ctx, event_name):
    """Updates the status.
    
    """
    status = GeneratorRunStatus(ctx.get_identifier(), event_name, datetime.datetime.now().timestamp())
    cache.set_run_status(status)


class OrchestrationStatusMiddleware(dramatiq.Middleware):
    """Middleware to automatically update the status of a generator.
    
    """
    def before_process_message(self, broker, message):
        """Called before a message is processed.

        :param broker: Message broker to which message was dispatched.
        :param message: A message being processed.

        """
        if isinstance(message.args, tuple) and len(message.args) > 0 and _get_actor_name(message).startswith("on_"):
            args = message.args if isinstance(message.args[0], GeneratorRun) else message.args[0]['args']
            if isinstance(args[0], GeneratorRun):
                do_update_status.send_with_options(
                    args=(args[0], _get_actor_name(message))
                    )        
            

def _get_actor_name(message):
    """Returns actor name by parsing incoming message.
    
    """
    return str(message).split('(')[0]

