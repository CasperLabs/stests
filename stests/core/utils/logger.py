import datetime as dt
import enum
import os
import sys
import typing



# Set of logging levels.
LOG_LEVEL_DEBUG = 'DEBUG'
LOG_LEVEL_INFO = 'INFO'
LOG_LEVEL_WARNING = 'WARN'
LOG_LEVEL_ERROR = 'ERROR'
LOG_LEVEL_CRITICAL = 'CRITICAL'
LOG_LEVEL_FATAL = 'FATAL'

# Text to display when passed a null message.
_NULL_MSG = '-------------------------------------------------------------------------------'


class SubSystem(enum.Enum):
    """Enumeration over set of set of sub-systems to report for logging purposes.
    
    """
    BROKER = enum.auto()
    CLX = enum.auto()
    CACHE = enum.auto()
    GENERATOR = enum.auto()
    MONITORING = enum.auto()


def log(msg: str = None, level: str = LOG_LEVEL_INFO):
    """Outputs a message to log.

    :param str msg: Message to be written to log.
    :param str level: Message level (e.g. INFO).

    """
    # TODO use structlog/logstash.
    print(_get_message(msg, level))


def log_debug(msg: str):
    """Outputs a debug message to log.

    :param str msg: Message to be written to log.

    """
    log(msg, LOG_LEVEL_DEBUG)


def log_error(err: typing.Union[str, Exception]):
    """Logs a runtime error.

    :param str err: Error to be written to log.

    """
    if issubclass(BaseException, err.__class__):
        msg = f"{err.__class__} :: {err}"
    else:
        msg = f"{err}"
    log(msg, LOG_LEVEL_ERROR)


def log_warning(err: typing.Union[str, Exception]):
    """Logs a runtime warning.

    :param str err: Warning to be written to log.

    """
    if issubclass(BaseException, err.__class__):
        msg = f"{err.__class__} :: {err}"
    else:
        msg = f"{err}"
    log(msg, LOG_LEVEL_WARNING)


def _get_message(msg: str, level: str) -> str:
    """Returns a formatted logging message.

    """
    if msg is None:
        return _NULL_MSG

    return f"{dt.datetime.utcnow()} [{level}] [{str(os.getpid()).zfill(5)}] STESTS {str(msg).strip()}"