import enum

import dramatiq

from stests.core.mq.brokers import get_broker
from stests.core.mq import encoder
from stests.core.utils import logger



def execute():
    """Initialises MQ broker & connects dramatiq library.

    """
    # Instantiate a broker.
    broker = get_broker()
    dramatiq.set_broker(broker)

    # Inject middleware.
    from stests.core.mq.middleware import get_middleware
    for mware in get_middleware():
        broker.add_middleware(mware)
    
    # Inject encoder.
    dramatiq.set_encoder(encoder)
