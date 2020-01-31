from dramatiq.brokers.redis import RedisBroker

from stests.core.utils import env



# Environment variables required by this module.
class EnvVars:
    # RabbitMQ host.
    DB = env.get_var('BROKER_REDIS_DB', 0, int)

    # RabbitMQ protocol.
    HOST = env.get_var('BROKER_REDIS_HOST', "amqp")

    # RabbitMQ port.
    PORT = env.get_var('BROKER_REDIS_PORT', 5672, int)


def get_broker(network_id: str) -> RedisBroker:
    """Returns instance of redis MQ broker.
    
    :param network_id: Identifier of network being tested, e.g. DEV-LOC-01
    :returns: An instance of a redis MQ broker.

    """
    # TODO: map network identifier to db#.
    return RedisBroker(
        db=EnvVars.DB,
        host=EnvVars.HOST,
        port=EnvVars.PORT
        )
