from dramatiq.brokers.redis import RedisBroker

from stests.core.mq.brokers.redis import connection



def get_broker(network_id: str) -> RedisBroker:
    """Returns instance of redis mq broker.
    
    :param network_id: Network identifier, e.g. LOC-DEV-01
    :returns: An instance of a redis MQ broker.

    """
    # TODO: map network identifier to db#.
    return RedisBroker(
        db=connection.DB,
        host=connection.HOST,
        port=connection.PORT
        )
