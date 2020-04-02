import enum

import dramatiq

from stests.core.mq.brokers import get_broker
from stests.core.mq import encoder
from stests.core.utils import logger



def execute():
    """Initialises MQ broker & connects dramatiq library.

    """
    # JIT import to avoid circularity - TODO remove.
    from stests.core.mq.middleware import get_middleware

    # Configure broker.
    broker = get_broker()
    for mware in get_middleware():
        broker.add_middleware(mware)
    
    # Configure dramatiq.
    dramatiq.set_broker(broker)
    dramatiq.set_encoder(encoder)
