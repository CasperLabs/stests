import abc
import datetime
import enum
import uuid
from dataclasses import dataclass
from dataclasses import field
from dataclasses_json import config
from dataclasses_json import dataclass_json
from datetime import datetime

from marshmallow import fields



def get_enum_field(enum: enum.Enum, default: str=None) -> field:
    """Returns an enumeration dataclass field with implicit encoding support.
    
    :param enum: An enum or flag being declared within a dataclass.
    :param default: Dataclass field's default value.

    """
    if default is not None:
        return field(
            default = default,
            metadata=config(
                encoder=lambda x: str(x),
                decoder=lambda x: enum[x.split('.')[-1]]
            ))
    return field(
        metadata=config(
            encoder=lambda x: str(x),
            decoder=lambda x: enum[x.split('.')[-1]]
        ))


def get_isodatetime_field(set_default=False):
    """Returns an ISO datetime field.
    
    :param default_factory: Factory method when underlying field value is initialised.

    """
    if set_default == True:
        return field(
            default_factory=datetime.now,
            metadata=config(
                encoder=datetime.isoformat,
                decoder=datetime.fromisoformat,
                mm_field=fields.DateTime(format='iso')
            )
        )
    return field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )


def get_uuid_field(set_default=False):
    """Returns a UUID4 field.
    
    :param default_factory: Factory method when underlying field value is initialised.

    """
    if set_default == True:
        return field(
            default_factory=lambda: str(uuid.uuid4()),
        )
    return field()


@dataclass_json
@dataclass
class Entity(abc.ABC):
    """Base class for all domain entities flowing through system.
    
    """
    pass
