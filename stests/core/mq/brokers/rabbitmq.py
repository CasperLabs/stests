from dramatiq.brokers.rabbitmq import RabbitmqBroker

from stests.core.utils import env



# Environment variables required by this module.
class EnvVars:
    # RabbitMQ host.
    HOST = env.get_var('BROKER_RABBIT_HOST', "localhost")

    # RabbitMQ port.
    PORT = env.get_var('BROKER_RABBIT_PORT', 5672, int)

    # RabbitMQ protocol.
    PROTOCOL = env.get_var('BROKER_RABBIT_PROTOCOL', "amqp")

    # RabbitMQ SSL client cert.
    SSL_CLIENT_CERT = env.get_var('BROKER_RABBIT_SSL_CLIENT_CERT')

    # RabbitMQ SSL client cert key.
    SSL_CLIENT_KEY = env.get_var('BROKER_RABBIT_SSL_CLIENT_KEY')

    # RabbitMQ user.
    USER = env.get_var('BROKER_RABBIT_USER', "stests-mq-user")

    # RabbitMQ user password.
    USER_PWD = env.get_var('BROKER_RABBIT_USER_PWD', "clabs")

    # RabbitMQ host.
    VHOST = env.get_var('BROKER_RABBIT_VHOST', "CLABS")



def get_broker() -> RabbitmqBroker:
    """Returns instance of rabbit MQ broker.

    :returns: An instance of a Rabbit MQ broker.

    """
    return RabbitmqBroker(url=_get_url())


def _get_url() -> str:
    """Returns rabbit MQ connection URL.
    
    """
    # TODO: apply ssl (if defined in env vars)
    return f"{EnvVars.PROTOCOL}://{EnvVars.USER}:{EnvVars.USER_PWD}@{EnvVars.HOST}:{EnvVars.PORT}/{EnvVars.VHOST}"
