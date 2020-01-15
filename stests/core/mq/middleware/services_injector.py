import dramatiq

from stests.core import cache
from stests.core.utils.execution import ExecutionContext



class ServicesInjectorMiddleware(dramatiq.Middleware):
    """Middleware to make available to actors services orthogonal to the execution context.
    
    """
    def before_process_message(self, broker, message):
        """Called before a message is processed.

        :param broker: Message broker to which message was dispatched.
        :param message: A message being processed.

        """
        # The execution context has already been deserialised by this point, therefore
        # we can use it to inject service proxies which are then available to actors.
        # Note: comprehension is used as position of execution context may very.
        for ctx in (i for i in message.args if isinstance(i, ExecutionContext)):
            ctx.services.cache = cache.get_store(ctx) 


def get_mware() -> ServicesInjectorMiddleware:
    """Returns instance of services injector middleware.
    
    """
    return ServicesInjectorMiddleware()
