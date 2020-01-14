from stests.core.utils import env



def _get_env_var(name, default=None):
    """Returns an environment variable's current value.

    """
    # Apply prefix.
    name = f'MQ_BROKER_RABBIT_{name}'

    return env.get_var(name, default)


# Config: rabbitmq host.
HOST = _get_env_var('HOST', "localhost")

# Config: rabbitmq port.
PORT = _get_env_var('PORT', 5672)

# Config: rabbitmq protocol.
PROTOCOL = _get_env_var('PORT', "amqp")

# Config: rabbitmq client ssl certificate.
SSL_CLIENT_CERT = _get_env_var('SSL_CLIENT_CERT', None)

# Config: rabbitmq client ssl key.
SSL_CLIENT_KEY = _get_env_var('SSL_CLIENT_KEY', None)

# Config: rabbitmq user.
USER = _get_env_var('PORT', "clabs-mq-stests-user")

# Config: rabbitmq user password.
USER_PWD = _get_env_var('PORT', "clabs")


def get_url(vhost):
    """Returns rabbit mq connection information.
    
    :param vhost: Broker virtual host to which to connect.

    """
    # TODO: ssl
    return f"{PROTOCOL}://{USER}:{USER_PWD}@{HOST}:{PORT}/{vhost}"
