import typing

import dramatiq

from stests.core.mq.middleware.actor_logging import get_mware as ActorLoggingMiddleware
from stests.core.mq.middleware.group_callbacks import get_mware as GroupCallbacksMiddleware



# Middleware to inject when processing simulation related messages.
MWARE = (
    ActorLoggingMiddleware,
    GroupCallbacksMiddleware,    
)


def get_middleware() -> typing.Tuple[dramatiq.Middleware]:
    """Returns set of middleware to be injected into dramatiq.

    :param mode: Mode in which MQ package is being used.
    
    """    
    return tuple(map(lambda T: T(), MWARE))
