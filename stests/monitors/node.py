import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.cache import NetworkIdentifier
from stests.core.utils import logger


# Queue to which messages will be dispatched.
_QUEUE = "monitoring.node"