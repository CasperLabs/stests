import dramatiq

from stests.core.mq import brokers
from stests.core.mq import encoder
from stests.core.utils.workflow import WorkflowContext



def init(ctx: WorkflowContext) -> dramatiq:
    """Wires dramatiq to message broker.
    
    :param network_id: Identifier of network being tested.
    :returns: Pointer to a configured dramatiq instance.

    """
    broker = brokers.get_broker(ctx)
    dramatiq.set_broker(broker)
    dramatiq.set_encoder(encoder)

    return dramatiq
