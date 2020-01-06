from enum import Enum

from stests.core.mq.brokers import rabbitmq
from stests.core.mq.brokers import redis
from stests.core.mq.brokers import stub


# Enum: set of supported mq broker types.
BrokerTypeEnum = Enum("BrokerTypeEnum", "rabbitmq redis stub")

# Map: Broker type -> factory.
FACTORIES = {
    BrokerTypeEnum.rabbitmq: rabbitmq,
    BrokerTypeEnum.redis: redis,
    BrokerTypeEnum.stub: stub
}


def get_broker(
    network_id: str,
    broker_type: BrokerTypeEnum = BrokerTypeEnum.rabbitmq
    ):
    """Returns an MQ broker instance for integration with dramatiq framework.

    """
    try:
        factory = FACTORIES[broker_type]
    except KeyError:
        raise NotImplementedError(f"{broker_type} MQ broker is unsupported")

    return factory.get_broker(network_id)
