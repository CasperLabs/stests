from dramatiq.brokers.redis import RedisBroker

from stests.core.utils import env



# Environment variables required by this module.
class EnvVars:
    # Redis host.
    DB = env.get_var('BROKER_REDIS_DB', 0, int)

    # Redis protocol.
    HOST = env.get_var('BROKER_REDIS_HOST', "localhost")

    # Redis port.
    PORT = env.get_var('BROKER_REDIS_PORT', 6379, int)



def get_broker() -> RedisBroker:
    """Returns instance of redis MQ broker.
    
    :param network_id: Identifier of network being tested, e.g. DEV-LOC-01
    :returns: An instance of a redis MQ broker.

    """
    return RedisBroker(
        db=EnvVars.DB,
        host=EnvVars.HOST,
        port=EnvVars.PORT
        )
