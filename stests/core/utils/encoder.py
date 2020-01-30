import typing

from stests.core.types import ENUMS
from stests.core.types import TYPESET as CORE_TYPESET



# Set typeset.
TYPESET = CORE_TYPESET

# Set typemap.
# Map: domain type keys -> domain type.  
TYPEMAP = {f"{i.__module__}.{i.__name__}": i for i in TYPESET}


def decode(data: typing.Any) -> typing.Any:
    """Decodes input data dispatched over wire.
    
    """
    # Recurse over tuples/lists.
    if isinstance(data, tuple):
        return tuple(map(decode, data))
    elif isinstance(data, list):
        return list(map(decode, data))

    # Skip all except dictionaries with injected type field.
    if not isinstance(data, dict) or '_type' not in data:
        return data

    # Get type to be instantiated.
    cls = TYPEMAP[data['_type']]
    
    # Return type instance hydrated from incoming data.
    return cls.from_dict(data)


def encode(data: typing.Any) -> typing.Any:
    """Encodes input data in readiness for dispatch over wire.
    
    """
    # Recurse over tuples/lists.
    if isinstance(data, tuple):
        return tuple(map(encode, data))
    elif isinstance(data, list):
        return list(map(encode, data))

    # Skip non domain types.
    if type(data) not in TYPESET:
        return data

    # Stringify domain enums.
    if type(data) in ENUMS:
        return str(data)

    # Dictionarify domain types.
    obj = data.to_dict()

    # Append domain info for downstream round-trip.
    obj['_type'] = f"{data.__module__}.{data.__class__.__name__}"

    return obj


def register_type(cls):
    """Workflows need to extend the typeset so as to ensure that arguments are decoded/encoded correctly.
    
    """
    global TYPESET
    if cls not in TYPESET:
        TYPESET = TYPESET | { cls, }
        TYPEMAP[f"{cls.__module__}.{cls.__name__}"] = cls
