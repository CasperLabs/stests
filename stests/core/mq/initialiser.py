import dramatiq

from stests.core.mq import brokers
from stests.core.mq import encoder



def init() -> dramatiq:
    """Wires dramatiq to message broker.
    
    :returns: Pointer to a configured dramatiq instance.

    """
    dramatiq.set_broker(brokers.get_broker())
    dramatiq.set_encoder(encoder)

    return dramatiq
