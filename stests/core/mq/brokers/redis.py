from dramatiq.brokers.redis import RedisBroker



def get_broker(network_id: str) -> RedisBroker:
    """Returns instance of redis mq broker.
    
    """
    raise NotImplementedError()
