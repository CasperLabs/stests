import os

from dramatiq.brokers.rabbitmq import RabbitmqBroker

from stests.utils.env import get_env_var



def get_broker(network_id: str) -> RabbitmqBroker:
    """Returns instance of rabbit mq broker.
    
    """
    # Set RabbitMQ virtual host.
    vhost = network_id.upper()

    # Set RabbitMQ connection url.
    url = _get_url(vhost)

    return RabbitmqBroker(url=url)


def _get_url(vhost):
    """Returns rabbit mq connection information.
    
    """
    # TODO: ssl
    return f"{_PROTOCOL}://{_USER}:{_USER_PWD}@{_HOST}:{_PORT}/{vhost}"


def _get_env_var(name, default=None):
    """Returns an environment variable's current value.

    """
    # Apply prefix.
    name = f'MQ_BROKER_RABBIT_{name}'

    return get_env_var(name, default)


# Broker config: protocol.
_PROTOCOL = _get_env_var('PROTOCOL', "amqp")

# Broker config: host.
_HOST = _get_env_var('HOST', "localhost")

# Broker config: port.
_PORT = _get_env_var('PORT', 5672)

# Broker config: user.
_USER = _get_env_var('USER', "clabs-mq-stests-user")

# Broker config: user password.
_USER_PWD = _get_env_var('USER_PWD', "clabs")

# Broker config: SSL client cert.
_SSL_CLIENT_CERT = _get_env_var('SSL_CLIENT_CERT')

# Broker config: SSL client key.
_SSL_CLIENT_KEY = _get_env_var('SSL_CLIENT_KEY')
