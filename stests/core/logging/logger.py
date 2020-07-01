import typing

from stests import events
from stests.core.logging.factory import get_message
from stests.core.logging.handlers import get_handler
from stests.core.types.logging import OutputMode



# Mode - determines output format.
_mode = OutputMode.INTERACTIVE


def log_event(event_type: events.EventType, message: typing.Optional[typing.Union[Exception, str]], *args, **kwargs):
    """Appends event information to event log.

    :param event_type: Type of event being logged.
    :param message: Message to be written to log.

    """
    get_handler(_mode).log_event(
        get_message(
            events.get_event_info(event_type, message, *args, **kwargs)
            ),
        _mode
        )

    
def initialise(mode: OutputMode):
    """Initialises logger.

    """
    global _mode

    _mode = mode
