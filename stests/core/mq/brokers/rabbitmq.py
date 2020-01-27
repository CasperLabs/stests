import os

from dramatiq.brokers.rabbitmq import RabbitmqBroker

from stests.core.utils import env
from stests.core.utils.workflow import WorkflowContext



def get_broker(ctx: WorkflowContext) -> RabbitmqBroker:
    """Returns instance of rabbit mq broker.

    :param ctx: Contextual information passed along the flow of execution.

    :returns: An instance of a Rabbit MQ broker.

    """
    # Set RabbitMQ virtual host.
    vhost = ctx.network_id.upper()

    # Set RabbitMQ connection url.
    url = _get_url(vhost)

    return RabbitmqBroker(url=url)


def _get_env_var(name, default=None, convertor=None):
    """Returns an environment variable's current value.

    """
    # Apply prefix.
    name = f'MQ_BROKER_RABBIT_{name}'

    return env.get_var(name, default, convertor)


# Config: rabbitmq host.
HOST = _get_env_var('HOST', "localhost")

# Config: rabbitmq port.
PORT = _get_env_var('PORT', 5672, int)

# Config: rabbitmq protocol.
PROTOCOL = _get_env_var('PORT', "amqp")

# Config: rabbitmq client ssl certificate.
SSL_CLIENT_CERT = _get_env_var('SSL_CLIENT_CERT', None)

# Config: rabbitmq client ssl key.
SSL_CLIENT_KEY = _get_env_var('SSL_CLIENT_KEY', None)

# Config: rabbitmq user.
USER = _get_env_var('USER', "clabs-mq-stests-user")

# Config: rabbitmq user password.
USER_PWD = _get_env_var('USER_PWD', "clabs")


def _get_url(vhost) -> str:
    """Returns rabbit mq connection URL.
    
    """
    # TODO: ssl
    return f"{PROTOCOL}://{USER}:{USER_PWD}@{HOST}:{PORT}/{vhost}"
