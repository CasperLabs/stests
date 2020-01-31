from dramatiq.broker import Broker

from stests.core.mq.brokers import rabbitmq
from stests.core.mq.brokers import redis
from stests.core.mq.brokers import stub
from stests.core.mq.middleware import get_middleware
from stests.core.utils import env
from stests.core.utils.exceptions import InvalidEnvironmentVariable



# Environment variables required by this module.
class EnvVars:
    # Cache type.
    TYPE = env.get_var("BROKER_TYPE", "RABBIT")


# Map: Broker type -> factory.
FACTORIES = {
    "RABBIT": rabbitmq,
    "REDIS": redis,
    "STUB": stub
}


def get_broker(network_id: str) -> Broker:
    """Returns an MQ broker instance for integration with dramatiq framework.

    :param network_id: Identifier of network being tested, e.g. DEV-LOC-01
    :returns: A configured message broker.

    """
    try:
        factory = FACTORIES[EnvVars.TYPE]
    except KeyError:
        raise InvalidEnvironmentVariable("BROKER_TYPE", EnvVars.TYPE, FACTORIES)

    broker = factory.get_broker(network_id)
    for mware in get_middleware():
        broker.add_middleware(mware)

    return broker
