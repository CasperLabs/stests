import dataclasses
import logging
import typing

import logstash

from stests.core.types.logging import Level
from stests.core.types.logging import LogMessage
from stests.core.types.logging import OutputMode
from stests.core.utils import env



# Logger instance. 
_logger: typing.Optional[logging.Logger] = None

# Map: log level -> log writer.
_writers: typing.Optional[dict] = None

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

    # Set writer.
    try:
        writer = _writers[msg.event.level]
    except KeyError:
        raise ValueError(f"Invalid log message event level: {msg.event.level}")

    # Emit log event.
    writer(msg.event.type, extra={'stests': dataclasses.asdict(msg)})


def _initialise() -> logging.Logger:
    """JIT initialiser.
    
    """
    global _logger
    global _writers

    # Set logger.
    _logger = logging.getLogger('STESTS')
    _logger.setLevel(logging.INFO)
    _logger.addHandler(logstash.UDPLogstashHandler(
        EnvVars.HOST,
        EnvVars.PORT,
        version=EnvVars.VERSION
        ))

    # Set writer map.
    _writers = {
        Level.DEBUG.name: _logger.debug,
        Level.INFO.name: _logger.info,
        Level.WARN.name: _logger.warning,
        Level.ERROR.name: _logger.error,
        Level.CRITICAL.name: _logger.critical,
        Level.FATAL.name: _logger.critical,
    }
