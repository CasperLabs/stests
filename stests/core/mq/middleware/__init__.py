import typing

import dramatiq

from stests.core.mq.middleware.group_callbacks import get_mware as GroupCallbacksMiddleware
from stests.core.mq.middleware.orchestration_status import OrchestrationStatusMiddleware
from stests.core.mq.middleware.results import get_mware as ResultsMiddleware
from stests.core.mq.middleware.logger import LoggingMiddleware



# Middleware to inject.
MWARE = (
    OrchestrationStatusMiddleware,
    LoggingMiddleware,
    # ResultsMiddleware,
    GroupCallbacksMiddleware,
)


def get_middleware() -> typing.Tuple[dramatiq.Middleware]:
    """Returns set of middleware to be injected into dramatiq.
    
    """
    return tuple(map(lambda T: T(), MWARE))
