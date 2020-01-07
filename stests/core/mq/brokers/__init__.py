from enum import Enum

from stests.core.mq.brokers import rabbitmq
from stests.core.mq.brokers import redis
from stests.core.mq.brokers import stub


# Enum: set of supported mq broker types.
MessageBrokerType = Enum("MessageBrokerType", [
    "RABBIT",
    "REDIS",
    "STUB"
])


# Map: Broker type -> factory.
FACTORIES = {
    MessageBrokerType.RABBIT: rabbitmq,
    MessageBrokerType.REDIS: redis,
    MessageBrokerType.STUB: stub
}


def get_broker(
    network_id: str,
    broker_type: MessageBrokerType = MessageBrokerType.RABBIT
    ):
    """Returns an MQ broker instance for integration with dramatiq framework.

    :param network_id: Network identifier, e.g. LOC-DEV-01
    :param broker_type: Type of broker to be instantiated.

    """
    try:
        factory = FACTORIES[broker_type]
    except KeyError:
        raise NotImplementedError(f"{broker_type} MQ broker is unsupported")

    return factory.get_broker(network_id)
