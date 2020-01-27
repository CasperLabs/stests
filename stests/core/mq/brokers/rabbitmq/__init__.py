import os

from dramatiq.brokers.rabbitmq import RabbitmqBroker

from stests.core.mq.brokers.rabbitmq import envars
from stests.core.utils.workflow import WorkflowContext


def get_broker(ctx: WorkflowContext) -> RabbitmqBroker:
    """Returns instance of rabbit mq broker.

    :param ctx: Contextual information passed along the flow of execution.

    :returns: An instance of a Rabbit MQ broker.

    """
    vhost = ctx.network_id.upper()
    url = _get_url(vhost)

    return RabbitmqBroker(url=url)


def _get_url(vhost) -> str:
    """Returns rabbit mq connection URL.
    
    """
    # TODO: ssl
    return f"{envars.PROTOCOL}://{envars.USER}:{envars.USER_PWD}@{envars.HOST}:{envars.PORT}/{vhost}"
