from dataclasses import field
from dataclasses_json import config
from enum import Enum



def get_enum_field(enum: Enum, default: str=None) -> field:
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
