import abc
import datetime
import enum
import uuid
import dataclasses
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime

from marshmallow import fields



def get_enum_field(enumfield: enum.Enum) -> field:
    """Returns an enumeration dataclass field with implicit encoding support.
    
    :param enum: An enum or flag being declared within a dataclass.

    :returns: Dataclass field.

    """
    return field(
        metadata=config(
            encoder=lambda x: x.name,
            decoder=lambda x: enumfield[x]
        ))


def _decode_enum_field(enumfield, x):
    try:
        return enumfield[x]
    except KeyError:
        return enumfield(x)


def get_isodatetime_field(set_default=False) -> field:
    """Returns an ISO datetime field.
    
    :param default_factory: Factory method when underlying field value is initialised.

    :returns: Dataclass field.

    """
    if set_default == True:
        return field(
            default_factory=lambda: datetime.now().timestamp(),
        )
    return field()


def get_uuid_field(set_default=False) -> field:
    """Returns a UUID4 field.
    
    :param default_factory: Factory method when underlying field value is initialised.

    :returns: Dataclass field.

    """
    if set_default == True:
        return field(
            default_factory=lambda: str(uuid.uuid4()),
        )
    return field()


@dataclass
class Entity(abc.ABC):
    """Base class for all domain entities flowing through system.
    
    """
    pass

