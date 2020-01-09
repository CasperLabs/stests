from dramatiq.brokers.stub import StubBroker
from stests.core.utils.execution import ExecutionContext



def get_broker(ctx: ExecutionContext) -> StubBroker:
    """Returns instance of stub mq broker, primarily for use in testing.
    
    :param network_id: Network identifier, e.g. LOC-DEV-01
    :returns: An instance of a stub MQ broker.

    """
    # TODO: incorporate network identifier.
    return StubBroker()
