import dramatiq

from stests.core import cache
from stests.core.utils.execution import ExecutionContext
from stests.core.utils import logger as _logger



class LoggingMiddleware(dramatiq.Middleware):
    """Middleware to make available to actors services orthogonal to the execution context.
    
    """
    def after_process_message(self, broker, message, *, result=None, exception=None):
        """Called after a message has been processed.

        :param broker: Message broker to which message was dispatched.
        :param message: A message being processed.

        """
        actor_name = str(message).split('(')[0]
        if exception is None:
            msg = f"{actor_name} :: EXECUTION COMPLETE"
            _logger.log(msg)
        else:
            msg = f"{actor_name} :: EXECUTION ERROR :: err={exception}"
            _logger.log_error(msg)


    def before_process_message(self, broker, message):
        """Called before a message is processed.

        :param broker: Message broker to which message was dispatched.
        :param message: A message being processed.

        """
        actor_name = str(message).split('(')[0]
        msg = f"{actor_name} :: EXECUTION STARTS"
        _logger.log(msg)


def get_mware() -> LoggingMiddleware:
    """Returns instance of services injector middleware.
    
    """
    return LoggingMiddleware()
