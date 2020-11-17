import functools
import time
import typing

from stests.chain import constants
from stests.core.utils.misc import Timer
from stests.core.types.chain import Account
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.events import EventType



class DeployDispatchInfo():
    """Encapsulates information required when dispatching a deploy.

    """
    def __init__(self,
        dispatcher: Account,
        network: Network,
        node: Node,
        time_to_live: str = constants.DEFAULT_TX_TIME_TO_LIVE,
        fee: str = constants.DEFAULT_TX_FEE,
        gas_price: int = constants.DEFAULT_TX_GAS_PRICE,
        ):
        """Instance constructor.

        """
        self.dispatcher = dispatcher
        self.network = network
        self.node = node
        self.node_address = node.url_rpc
        self.time_to_live = time_to_live
        self.fee = fee
        self.gas_price = gas_price


class CLI_Exception(Exception):
    """Command line interface exception class.

    """

    def __init__(self,
        command: str,
        event_type: EventType,
        attempts: int,
        err: Exception,
        ):
        """Constructor.

        :param msg: Exception message.

        """
        self.attempts = attempts
        self.command = command
        self.message = f"{command} failed after {attempts} attempts :: {err}"
        self.err = err
        self.event_type = event_type


    def __str__(self):
        """Returns a string representation.

        """
        return u"STESTS CLI EXCEPTION : {0}".format(repr(self.message))


def execute_cli(command: str, on_failure_event: EventType,  max_attempts: int = 5, retry_delay: float = 1.0) -> typing.Callable:
    """Decorator to orthoganally execute a CLI operation.

    :param command: CLI command being executed.
    :param on_failure_event: Logging event to emit upon failure.
    :param max_attempts: Maximum attempts to try being escaping.
    :param retry_delay: Retry delay.

    :returns: Decorated function with it's result augmented with execution stats.

    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            with Timer() as timer:
                attempts = 0
                while attempts < max_attempts:
                    attempts += 1
                    try:
                        result = func(*args, **kwargs)
                    except Exception as err:
                        if attempts == max_attempts:
                            raise CLI_Exception(command, on_failure_event, attempts, err)
                        time.sleep(retry_delay)
                    else:
                        break

            return result, timer.elapsed, attempts

        return wrapper
    return decorator
