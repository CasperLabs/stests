from dataclasses import field
from enum import Enum

from dataclasses_json import config



def get_enum_field(enum: Enum, default: str=None) -> field:
    """Returns an enumeration dataclass field with implicit 
       encoding support to simplify instance <-> json.
    
    :param enum: An enum being declared within a dataclass.
    :param default: Dataclass field's default value.

    """
    return field(
        default = default,
        metadata=config(
            encoder=lambda x: str(x).split('.')[-1],
            decoder=lambda x: enum[x]
        ))
