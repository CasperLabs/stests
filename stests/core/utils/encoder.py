import inspect
import typing

from stests.core.types import ENUMS
from stests.core.types import TYPESET as CORE_TYPESET



# Set typeset.
TYPESET = CORE_TYPESET

# Map: domain type keys -> domain type.  
TYPEMAP = {f"{i.__module__}.{i.__name__}": i for i in TYPESET}

# Map: domain enum keys -> enum.  
ENUMMAP = dict()
for i in ENUMS:
    for j in i:
        ENUMMAP[str(j)] = j    


def decode(data: typing.Any) -> typing.Any:
    """Decodes input data dispatched over wire.
    
    """
    # Recurse over tuples/lists.
    if isinstance(data, tuple):
        return tuple(map(decode, data))
    elif isinstance(data, list):
        return list(map(decode, data))

    # Skip all except dictionaries with injected type field.
    if isinstance(data, dict) and '_type' in data:
        return _decode_domain_class(data)

    # Map stringified enum values.
    if isinstance(data, str) and data in ENUMMAP:
        return ENUMMAP[data]

    return data


def _decode_domain_class(data):
    """Decodes a domain class by performing a type lookup.
    
    """
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

    # Map domain types to dictionary.
    obj = data.to_dict()

    # Inject type info used when decoding.
    obj['_type'] = f"{data.__module__}.{data.__class__.__name__}"

    return obj


def register_type(cls):
    """Workflows need to extend the typeset so as to ensure that arguments are decoded/encoded correctly.
    
    """
    global TYPESET
    if cls not in TYPESET:
        TYPESET = TYPESET | { cls, }
        TYPEMAP[f"{cls.__module__}.{cls.__name__}"] = cls
