import typing

import dramatiq

from stests.core.mq.middleware.mware_group_callbacks import get_mware as GroupCallbacksMiddleware
from stests.core.mq.middleware.mware_logger import LoggingMiddleware



# Middleware to inject when processing monitoring related messages.
MWARE = (
    LoggingMiddleware,
    GroupCallbacksMiddleware,
)
