import dramatiq
from stests.core.domain import RunContext
from stests.generators.shared.actors.events_generator import do_persist_generator_event



class GeneratorEventMiddleware(dramatiq.Middleware):
    """Middleware to automatically persist generator events.
    
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
                do_persist_generator_event.send_with_options(
                    args=(args[0], _get_actor_name(message))
                    )        


def _get_actor_name(message):
    """Returns actor name by parsing incoming message.
    
    """
    return str(message).split('(')[0]
