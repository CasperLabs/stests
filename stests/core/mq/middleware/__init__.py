import typing

import dramatiq

from stests.core.mq.middleware.args_destructurer import ArgsDestructurerMiddleware
from stests.core.mq.middleware.logger import LoggingMiddleware



# Middleware to inject.
MWARE = (
    LoggingMiddleware,
    ArgsDestructurerMiddleware
)


def get_middleware() -> typing.Tuple[dramatiq.Middleware]:
    """Returns set of middleware to be injected into dramatiq.
    
    """
    return tuple(map(lambda T: T(), MWARE))
