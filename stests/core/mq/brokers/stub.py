from dramatiq.brokers.stub import StubBroker
from stests.core.utils.workflow import WorkflowContext



def get_broker(ctx: WorkflowContext) -> StubBroker:
    """Returns instance of stub mq broker, primarily for use in testing.
    
    :param network_id: Network identifier, e.g. DEV-LOC-01
    :returns: An instance of a stub MQ broker.

    """
    # TODO: incorporate network identifier.
    return StubBroker()
