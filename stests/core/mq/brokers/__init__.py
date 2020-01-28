from dramatiq.broker import Broker

from stests.core.mq.brokers import rabbitmq
from stests.core.mq.brokers import redis
from stests.core.mq.brokers import stub
from stests.core.mq.middleware import get_middleware
from stests.core.utils import env
from stests.core.utils.exceptions import InvalidEnvironmentVariable
from stests.core.utils.workflow import WorkflowContext


# Name of environment variable for deriving broker type.
EVAR_BROKER_TYPE = "MQ_BROKER_TYPE"

# Default type of message broker to instantiate.
DEFAULT_BROKER_TYPE = "RABBIT"

# Map: Broker type -> factory.
FACTORIES = {
    "RABBIT": rabbitmq,
    "REDIS": redis,
    "STUB": stub
}


def get_broker(ctx: WorkflowContext) -> Broker:
    """Returns an MQ broker instance for integration with dramatiq framework.

    :param ctx: Contextual information passed along the flow of execution.
    :returns: A configured message broker.

    """
    factory = FACTORIES[_get_broker_type()]
    broker = factory.get_broker(ctx)
    for mware in get_middleware():
        broker.add_middleware(mware)

    return broker


def _get_broker_type():
    """Interrogates environment variable to derive type of broker to instantiate.
    
    """    
    val = env.get_var(EVAR_BROKER_TYPE)
    if val is None:
        return DEFAULT_BROKER_TYPE
    if val not in FACTORIES:
        name = env.get_var_name(EVAR_BROKER_TYPE)
        raise InvalidEnvironmentVariable(name, val, FACTORIES)

    return val
