from dramatiq.broker import Broker

from stests.core.mq.brokers import rabbitmq
from stests.core.mq.brokers import redis
from stests.core.mq.brokers import stub
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


def get_broker() -> Broker:
    """Returns an MQ broker instance for integration with dramatiq framework.

    :returns: A configured message broker.

    """
    try:
        factory = FACTORIES[EnvVars.TYPE]
    except KeyError:
        raise InvalidEnvironmentVariable("BROKER_TYPE", EnvVars.TYPE, FACTORIES)

    return factory.get_broker()
