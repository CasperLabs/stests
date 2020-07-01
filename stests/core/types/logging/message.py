import dataclasses
import typing

from stests.core.types.logging.application_info import ApplicationInfo
from stests.core.types.logging.event_info import EventInfo
from stests.core.types.logging.process_info import ProcessInfo



@dataclasses.dataclass
class LogMessage:
    """Simple event log information for basic scenario.
    
    """
    # Application information.
    app: ApplicationInfo

    # Event information.
    event: EventInfo

    # Process information.
    process: ProcessInfo
    
    # Plain text message.
    message: typing.Optional[str]

    # Message data.
    data: typing.Dict[str, typing.Any]
