import os

from dramatiq.brokers.rabbitmq import RabbitmqBroker

from stests.core.mq.brokers.rabbitmq import evars



def get_broker(network_id: str) -> RabbitmqBroker:
    """Returns instance of rabbit MQ broker.

    :param network_id: Identifier of network being tested, e.g. DEV-LOC-01
    :returns: An instance of a Rabbit MQ broker.

    """
    url = _get_url(network_id)

    return RabbitmqBroker(url=url)


def _get_url(network_id) -> str:
    """Returns rabbit MQ connection URL.
    
    """
    # TODO: ssl
    return f"{evars.PROTOCOL}://{evars.USER}:{evars.USER_PWD}@{evars.HOST}:{evars.PORT}/{network_id}"
