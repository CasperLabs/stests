import abc
import datetime
import uuid
import dataclasses
from datetime import datetime



def get_isodatetime_field(set_default=False) -> dataclasses.field:
    """Returns an ISO datetime field.
    
    :param default_factory: Factory method when underlying field value is initialised.

    :returns: Dataclass field.

    """
    if set_default == True:
        return dataclasses.field(
            default_factory=lambda: datetime.now().timestamp(),
        )
    return dataclasses.field()


def get_uuid_field(set_default=False) -> dataclasses.field:
    """Returns a UUID4 field.
    
    :param default_factory: Factory method when underlying field value is initialised.

    :returns: Dataclass field.

    """
    if set_default == True:
        return dataclasses.field(
            default_factory=lambda: str(uuid.uuid4()),
        )
    return dataclasses.field()


@dataclasses.dataclass
class Entity(abc.ABC):
    """Base class for all domain entities flowing through system.
    
    """
    pass
