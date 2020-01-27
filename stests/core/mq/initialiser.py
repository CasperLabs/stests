import dramatiq

from stests.core.mq import encoder
from stests.core.mq import factory
from stests.core.mq.brokers import BrokerType
from stests.core.utils.workflow import WorkflowContext



def init(
    ctx: WorkflowContext,
    broker_type: BrokerType = BrokerType.RABBIT
    ) -> dramatiq:
    """Initialises message broker plus dramtiq.
    
    :param network_id: Identifier of network being tested.
    :param broker_type: Type of message broker to bind to.

    :returns: Pointer to a configured dramatiq instance.

    """
    # Set broker.
    broker = factory.get_broker(ctx, broker_type)

    # Configure dramatiq.
    dramatiq.set_broker(broker)
    dramatiq.set_encoder(encoder)

    return dramatiq
