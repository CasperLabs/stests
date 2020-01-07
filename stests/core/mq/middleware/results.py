from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend

from stests.core.mq.encoders import encoder_for_results
from stests.core.cache.redis.utils.connection import get_connection



def get_middleware():
    """Returns instance of results middleware configured with redis backend.
    
    """
    # Set backend.
    result_backend = RedisBackend(
        encoder=encoder_for_results,
        client=get_connection()
        )

    # Return configured middleware.
    return Results(backend=result_backend)
