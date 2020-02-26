import typing

import dramatiq

from stests.core.mq.middleware.mware_group_callbacks import get_mware as GroupCallbacksMiddleware
from stests.core.mq.middleware.mware_logger import LoggingMiddleware



# Middleware to inject when processing simulation related messages.
MWARE = (
    LoggingMiddleware,
    GroupCallbacksMiddleware,
)


def get_middleware() -> typing.Tuple[dramatiq.Middleware]:
    """Returns set of middleware to be injected into dramatiq.

    :param mode: Mode in which MQ package is being used.
    
    """    
    return tuple(map(lambda T: T(), MWARE))
