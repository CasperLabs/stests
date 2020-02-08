import inspect
import typing

from stests.core.types import ENUMS
from stests.core.types import TYPESET as CORE_TYPESET

from stests.core.domain import TYPESET as DOMAIN_TYPESET


# Set typeset.
TYPESET = CORE_TYPESET | DOMAIN_TYPESET

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
    if isinstance(data, tuple):
        return tuple(map(decode, data))

    if isinstance(data, list):
        return list(map(decode, data))

    if isinstance(data, dict) and '_type' in data:
        dclass = TYPEMAP[data['_type']]
        return dclass.from_dict(data)

    if isinstance(data, dict):
        return {k: decode(v) for k, v in data.items()}        

    if isinstance(data, str) and data in ENUMMAP:
        return ENUMMAP[data]

    return data


def encode(data: typing.Any) -> typing.Any:
    """Encodes input data in readiness for dispatch over wire.
    
    """
    if isinstance(data, tuple):
        return tuple(map(encode, data))

    if isinstance(data, list):
        return list(map(encode, data))

    if type(data) not in TYPESET:
        return data

    if type(data) in ENUMS:
        return str(data)

    # Inject type info for subsequent decoding operation.
    return {**data.to_dict(), **{
        '_type': f"{data.__module__}.{data.__class__.__name__}",
    }}


def register_type(cls):
    """Workflows need to extend the typeset so as to ensure that arguments are decoded/encoded correctly.
    
    """
    global TYPESET
    if cls not in TYPESET:
        TYPESET = TYPESET | { cls, }
        TYPEMAP[f"{cls.__module__}.{cls.__name__}"] = cls

