import dramatiq

from stests.core.mq.brokers import get_broker
from stests.core.mq.brokers import BrokerTypeEnum
from stests.core.mq.encoders import encoder_for_messages as encoder
from stests.core.mq.middleware import get_middleware



def init(
    network_id: str,
    broker_type: BrokerTypeEnum = BrokerTypeEnum.rabbitmq
    ) -> dramatiq:
    """Initialises message queue package.
    
    :param network_id: Identifier of network being tested.
    :param broker_type: Type of message broker to bind to.

    :returns: Pointer to a configured dramatiq instance.

    """
    # Set message broker.
    broker = get_broker(network_id, broker_type)

    # Set message broker middleware.
    for mware in get_middleware():
        broker.add_middleware(mware)

    # Wire up dramatiq.
    dramatiq.set_broker(broker)
    dramatiq.set_encoder(encoder)

    return dramatiq