from dramatiq.brokers.redis import RedisBroker

from stests.core.mq.brokers.redis import envars
from stests.core.utils.workflow import WorkflowContext


def get_broker(ctx: WorkflowContext) -> RedisBroker:
    """Returns instance of redis mq broker.
    
    :param ctx: Contextual information passed along the flow of execution.

    :returns: An instance of a redis MQ broker.

    """
    # TODO: map network identifier to db#.
    return RedisBroker(
        db=envars.DB,
        host=envars.HOST,
        port=envars.PORT
        )
