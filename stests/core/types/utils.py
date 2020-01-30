import enum
from dataclasses import dataclass
from dataclasses import field
from dataclasses_json import dataclass_json
from dataclasses_json import config
from datetime import datetime

from marshmallow import fields



def get_isodatetime_field(default_factory=datetime.now):
    """Returns an ISO datetime field.
    
    :param default_factory: Factory method when underlying field value is initialised.

    """
    return field(
        default_factory=default_factory,
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )


def get_enum_field(enum: enum.Enum, default: str=None) -> field:
    """Returns an enumeration dataclass field with implicit encoding support.
    
    :param enum: An enum or flag being declared within a dataclass.
    :param default: Dataclass field's default value.

    """
    return field(
        default = default,
        metadata=config(
            encoder=lambda x: str(x).split('.')[-1],
            decoder=lambda x: enum[x]
        ))


@dataclass_json
@dataclass
class Entity():
    """Base class for all entities flowing through system.
    
    """    
    # Timestamp when entity was first instantiated.
    _created_at: datetime = get_isodatetime_field()