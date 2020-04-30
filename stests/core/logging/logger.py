import dataclasses
import typing
from datetime import datetime

from stests import events
from stests.core.logging.factory import get_message
from stests.core.logging.types import OutputMode
from stests.core.utils import env


# Mode - determines output format.
_mode = OutputMode.INTERACTIVE


def log_event(event_type: events.EventType, message: typing.Optional[typing.Union[Exception, str]], *args, **kwargs):
    """Appends event information to event log.

    :param event_type: Type of event being logged.
    :param message: Message to be written to log.

    """
    # Must be JIT imported.
    # from stests.core.utils import encoder

    # Build log message.
    msg = get_message(events.get_event_info(event_type, message, *args, **kwargs))

    # Write to log.
    # TODO - use structlog | logstash ?
    if _mode == OutputMode.INTERACTIVE:
        print(f"{datetime.utcnow().isoformat()}Z [{msg.event.level}] [{msg.process.pid}] {msg.app.system} :: {msg.message}")
    else:
        print(f"{datetime.utcnow().isoformat()}Z {msg.event.level} {msg.event.priority} {msg.process.host} {msg.app.company.lower()}-{msg.app.system.lower()} {msg.app.sub_system.lower()} payload={dataclasses.asdict(msg)}")


def initialise(mode: OutputMode):
    """Initialises logger.

    """
    global _mode

    _mode = mode
