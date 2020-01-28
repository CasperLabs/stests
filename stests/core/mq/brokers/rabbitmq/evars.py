import typing

from stests.core.utils import env



def _get_env_var(
    name: str,
    default: typing.Any = None,
    convertor: typing.Callable = None
    ) -> str:
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
