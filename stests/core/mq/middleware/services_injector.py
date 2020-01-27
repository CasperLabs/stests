import dramatiq

from stests.core import cache
from stests.core.utils.workflow import WorkflowArguments
from stests.core.utils.workflow import WorkflowContext



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
        message.args = tuple(map(_get_ctx, message.args))



def _get_ctx(data):
    if isinstance(data, WorkflowArguments):
        return WorkflowContext.create(data)
    return data


def get_mware() -> ServicesInjectorMiddleware:
    """Returns instance of services injector middleware.
    
    """
    return ServicesInjectorMiddleware()
