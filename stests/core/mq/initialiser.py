import dramatiq

from stests.core.mq import brokers
from stests.core.mq import encoder



def execute():
    """Initialises dramatiq library.
    
    """
    # Simply broker & encoder.
    dramatiq.set_broker(brokers.get_broker())
    dramatiq.set_encoder(encoder)
