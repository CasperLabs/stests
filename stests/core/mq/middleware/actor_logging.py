import dramatiq

from stests.core.logging import log_event
from stests.events import EventType



class LoggingMiddleware(dramatiq.Middleware):
    """Middleware to make available to actors services orthogonal to the execution context.
    
    """
    def after_process_message(self, broker, message, *, result=None, exception=None):
        """Called after a message has been processed.

        :param broker: Message broker to which message was dispatched.
        :param message: A message being processed.

        """
        if exception is not None:
            log_event(EventType.CORE_ACTOR_ERROR, f"{_get_actor_name(message)} :: err={exception}")


def _get_actor_name(message):
    """Returns actor name by parsing incoming message.
    
    """
    return str(message).split('(')[0]


def get_mware():
    """Factory method invoked during broker initialisation.
    
    """
    return LoggingMiddleware()
