import enum

import dramatiq

from stests.core.mq.brokers import get_broker
from stests.core.mq import encoder
from stests.core.mq.mode import BrokerMode



def execute(mode: BrokerMode = BrokerMode.SIMULATION):
    """Initialises dramatiq library.

    :param mode: Mode in which MQ package is being used.
    
    """
    # Instantiate a broker.
    broker = get_broker()
    dramatiq.set_broker(broker)

    # Inject middleware.
    from stests.core.mq.middleware import get_middleware
    for mware in get_middleware(mode):
        broker.add_middleware(mware)

    # Simply broker & encoder.
    dramatiq.set_encoder(encoder)
