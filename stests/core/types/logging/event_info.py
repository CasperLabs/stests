import dataclasses
import datetime

from stests.core.types.logging.enums import Level



@dataclasses.dataclass
class EventInfo():
    """Encapsulates information pertaining to the application.
    
    """
    # Event id for disambiguation purpose.
    id: str

    # Event level.
    level: Level

    # Event priority.
    priority: int

    # ISO UTC Timestamp.
    timestamp: datetime.datetime

    # Event type for disambiguation purpose.
    type: str
