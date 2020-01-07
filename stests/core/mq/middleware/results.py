from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend

from stests.core.mq.brokers.redis.connection import get_connection
from stests.core.mq.encoders import encoder_for_results as encoder



def get_middleware():
    """Returns instance of results middleware configured with redis backend.
    
    """
    # Set backend.
    result_backend = RedisBackend(
        encoder=encoder,
        client=get_connection()
        )

    # Return configured middleware.
    return Results(backend=result_backend)
