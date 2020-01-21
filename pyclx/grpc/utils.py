import functools
import logging
import time
import typing

import grpc
from grpc._channel import _Rendezvous



# Maximum number of times to retry remote execution.
NUMBER_OF_RETRIES = 5

# Initial delay in seconds before an attempt to retry
INITIAL_DELAY = 0.3


def retry_unary(function) -> typing.Callable:
    """Function decorator to manage unary endpoint retries.
    
    """
    @functools.wraps(function)
    def wrapper(*args):
        return _retry_wrapper(function, *args)

    return wrapper


def retry_stream(function) -> typing.Callable:
    """Function decorator to manage stream endpoint retries.
    
    """
    @functools.wraps(function)
    def wrapper(*args):
        yield from _retry_wrapper(function, *args)

    return wrapper


def _retry_wrapper(function, *args) -> typing.Any:
    """Wraps an endpoint executor with retry semantics in case of channel faults.
    
    """
    delay = INITIAL_DELAY
    for i in range(NUMBER_OF_RETRIES):
        try:
            return function(*args)
        except _Rendezvous as err:
            if err.code() == grpc.StatusCode.UNAVAILABLE and i < NUMBER_OF_RETRIES - 1:
                delay += delay
                logging.warning(f"GRPC :: execution retry: delay={delay} seconds, fault={err}")
                time.sleep(delay)
            else:
                raise
