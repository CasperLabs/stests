import os
import platform
import pwd
import socket
import typing

from stests import __version__
from stests import events
from stests.core.logging.handlers import get_handler
from stests.core.types.logging import ApplicationInfo
from stests.core.types.logging import EventInfo
from stests.core.types.logging import Level
from stests.core.types.logging import LogMessage
from stests.core.types.logging import OutputMode
from stests.core.types.logging import ProcessInfo



# Mode - determines output format.
_mode = OutputMode.INTERACTIVE


def log_event(event_type: events.EventType, message: typing.Optional[typing.Union[Exception, str]], *args, **kwargs):
    """Appends event information to event log.

    :param event_type: Type of event being logged.
    :param message: Message to be written to log.

    """
    get_handler(_mode).log_event(
        _get_message(
            events.get_event_info(event_type, message, *args, **kwargs)
            ),
        _mode
        )

    
def initialise(mode: OutputMode):
    """Initialises logger.

    """
    global _mode

    _mode = mode


def _get_message(info: events.EventInfo) -> LogMessage:
    """Returns application information to be logged.
    
    """
    if info.priority >= Level.FATAL.value:
        level = Level.FATAL
    elif info.priority >= Level.CRITICAL.value:
        level = Level.CRITICAL
    elif info.priority >= Level.ERROR.value:
        level = Level.ERROR
    elif info.priority >= Level.WARN.value:
        level = Level.WARN
    elif info.priority >= Level.INFO.value:
        level = Level.INFO
    else:
        level = Level.DEBUG

    from stests.core.utils import encoder

    return LogMessage(
        app=ApplicationInfo(
            "STESTS",
            info.sub_system,
            __version__
        ),
        event=EventInfo(
            id=info.id,
            level=level.name,
            priority=info.priority,
            timestamp=info.timestamp,
            type=info.name,
        ),
        process=ProcessInfo(
            os_user=pwd.getpwuid(os.getuid())[0],
            pid=str(os.getpid()).zfill(5),
        ),
        message = info.message,
        data=encoder.encode(info.data, requires_decoding=False),
    )
