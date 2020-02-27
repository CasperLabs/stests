import typing
from dataclasses import dataclass

from stests.core.utils.domain import *



@dataclass
class RunEvent(Entity):
    """Event information associated with a generator run.
    
    """
    # Event name.
    event: str

    # Associated network.
    network: str

    # Numerical index to distinguish between multiple runs of the same generator.
    run: int

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str

    # Moment in time when event occurred.
    timestamp: int

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    # Timestamp: create.
    _ts_created: datetime = get_isodatetime_field()

    # Timestamp: update.
    _ts_updated: typing.Optional[datetime] = None

    # Universally unique identifier.
    _uid: str = get_uuid_field() 
