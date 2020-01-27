import dramatiq

from stests.core import cache
from stests.core.utils.workflow import WorkflowContext
from stests.core.utils import logger as _logger



class LoggingMiddleware(dramatiq.Middleware):
    """Middleware to make available to actors services orthogonal to the execution context.
    
    """
    def after_process_message(self, broker, message, *, result=None, exception=None):
        """Called after a message has been processed.

        :param broker: Message broker to which message was dispatched.
        :param message: A message being processed.

        """
        if exception is None:
            msg = f"ACTOR :: {_get_actor_name(message)} :: execution complete"
            _logger.log(msg)
        else:
            msg = f"ACTOR :: {_get_actor_name(message)} :: ERROR :: err={exception}"
            _logger.log_error(msg)


    def before_process_message(self, broker, message):
        """Called before a message is processed.

        :param broker: Message broker to which message was dispatched.
        :param message: A message being processed.

        """
        msg = f"ACTOR :: {_get_actor_name(message)} :: executing ..."
        _logger.log(msg)


def _get_actor_name(message):
    """Returns actor name by parsing incoming message.
    
    """
    return str(message).split('(')[0]


def get_mware() -> LoggingMiddleware:
    """Returns instance of services injector middleware.
    
    """
    return LoggingMiddleware()
