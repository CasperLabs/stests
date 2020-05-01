import dataclasses
from datetime import datetime
import logging
import sys
import typing

import logstash

from stests.core.logging.types import Level
from stests.core.logging.types import LogMessage
from stests.core.logging.types import OutputMode
from stests.core.utils import env


# Logger instance. 
_logger: typing.Optional[logging.Logger] = None


# Environment variables required by this module.
class EnvVars:
    # Logstash protocol.
    HOST = env.get_var('LOGGING_LOGSTASH_HOST', "localhost")

    # Logstash port.
    PORT = env.get_var('LOGGING_LOGSTASH_PORT', 5959, int)

    # Logstash version.
    VERSION = env.get_var('LOGGING_LOGSTASH_VERSION', 1, int)


def log_event(msg: LogMessage, mode: OutputMode):
    """Appends event information to event log.

    :param msg: Message to be logged.
    :param mode: Logging output mode as per execution host.

    """
    # JIT initialise.
    if _logger is None:
        _initialise()
    
    if msg.event.level == Level.DEBUG.name:
        writer = _logger.debug
    elif msg.event.level == Level.INFO.name:
        writer = _logger.info
    elif msg.event.level == Level.WARN.name:
        writer = _logger.warning
    elif msg.event.level == Level.ERROR.name:
        writer = _logger.error
    elif msg.event.level in (Level.CRITICAL.name, Level.FATAL.name):
        writer = _logger.critical
    else:
        raise ValueError(f"Invalid log message event level: {msg.event.level}")

    writer(f"{msg.app.system}:{msg.app.sub_system}:{msg.event.type}", extra={
        'stests': dataclasses.asdict(msg)
    })


def _initialise() -> logging.Logger:
    """JIT initialiser.
    
    """
    global _logger

    _logger = logging.getLogger('STESTS')
    _logger.setLevel(logging.INFO)
    _logger.addHandler(logstash.LogstashHandler(
        EnvVars.HOST,
        5959,
        version=EnvVars.VERSION
        ))
