from datetime import datetime
import typing

import dramatiq

from stests import chain
from stests.core import cache
from stests.core import factory
from stests.core.logging import log_event
from stests.core.types.chain import BlockStatus
from stests.core.types.chain import DeployStatus
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.types.infra import NodeEventInfo
from stests.events import EventType

from stests.core.types.chain import Deploy
from stests.core.types.infra import NodeIdentifier


# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.block.finalized"


@dramatiq.actor(queue_name=_QUEUE)
def on_block_finalized(info: NodeEventInfo):   
    """Event: raised whenever a block is finalized.

    :param info: Node event information.

    """
    return
