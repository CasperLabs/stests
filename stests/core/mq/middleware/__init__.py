import typing

import dramatiq

from stests.core.mq.middleware.args_destructurer import get_mware  as _get_args_destructurer
from stests.core.mq.middleware.logger import get_mware  as _get_logger
from stests.core.mq.middleware.services_injector import get_mware as _get_services_injector


def get_middleware() -> typing.Tuple[dramatiq.Middleware]:
    """Returns middleware to be applied to a broker.
    
    """
    return (
        _get_logger(),
        _get_args_destructurer(),
        _get_services_injector()
        )
