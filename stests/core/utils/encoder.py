import typing

from stests.core.types import ENUMS
from stests.core.types import TYPESET as CORE_TYPESET
from stests.core.utils.workflow import WorkflowContext
from stests.core.utils.workflow import WorkflowArguments



# Set typeset.
TYPESET = CORE_TYPESET

# Set typemap.
# Map: domain type keys -> domain type.  
TYPEMAP = {f"{i.__module__}.{i.__name__}": i for i in TYPESET}


def encode(data: typing.Any) -> bytes:
    """Encodes input data in readiness for dispatch over wire.
    
    """
    # Recurse over tuples/lists.
    if isinstance(data, tuple):
        return tuple(map(encode, data))
    elif isinstance(data, list):
        return list(map(encode, data))

    # When encoding workflow context simply encode the arguments.
    if isinstance(data, WorkflowContext):
        return encode(data.args)

    # Skip non-custom types.
    if type(data) not in TYPESET:
        return data

    if type(data) in ENUMS:
        return str(data)

    # Convert custom types to dictionary.
    obj = data.to_dict()

    # Append type info for downstream round-trip.
    obj['_type'] = f"{data.__module__}.{data.__class__.__name__}"

    return obj


def decode(data: bytes) -> typing.Any:
    """Decodes data dispatched over wire.
    
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


def register_type(cls):
    """Workflows need to extend the typeset so as to ensure that arguments are decoded/encoded correctly.
    
    """
    global TYPESET
    if cls not in TYPESET:
        TYPESET = TYPESET | { cls, }
        TYPEMAP[f"{cls.__module__}.{cls.__name__}"] = cls
