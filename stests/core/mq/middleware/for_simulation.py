import typing

import dramatiq

from stests.core.mq.middleware.mware_group_callbacks import get_mware as GroupCallbacksMiddleware
from stests.core.mq.middleware.mware_generator_event import GeneratorEventMiddleware
from stests.core.mq.middleware.mware_logger import LoggingMiddleware



# Middleware to inject when processing simulation related messages.
MWARE = (
    GeneratorEventMiddleware,
    LoggingMiddleware,
    GroupCallbacksMiddleware,
)
