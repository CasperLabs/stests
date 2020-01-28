from dramatiq.brokers.redis import RedisBroker

from stests.core.mq.brokers.redis import evars



def get_broker(network_id: str) -> RedisBroker:
    """Returns instance of redis MQ broker.
    
    :param network_id: Identifier of network being tested, e.g. DEV-LOC-01
    :returns: An instance of a redis MQ broker.

    """
    # TODO: map network identifier to db#.
    return RedisBroker(
        db=evars.DB,
        host=evars.HOST,
        port=evars.PORT
        )
