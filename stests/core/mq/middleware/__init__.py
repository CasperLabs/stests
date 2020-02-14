import typing

import dramatiq

from stests.core.mq.mode import BrokerMode



def get_middleware(mode: BrokerMode) -> typing.Tuple[dramatiq.Middleware]:
    """Returns set of middleware to be injected into dramatiq.

    :param mode: Mode in which MQ package is being used.
    
    """    
    if mode == BrokerMode.MONITORING:
        from stests.core.mq.middleware.for_monitoring import MWARE
    elif mode == BrokerMode.SIMULATION:
        from stests.core.mq.middleware.for_simulation import MWARE

    return tuple(map(lambda T: T(), MWARE))
