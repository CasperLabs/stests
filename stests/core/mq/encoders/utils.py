import typing

from stests.core.types import TYPEMAP
from stests.core.types import TYPESET



def encode(data: typing.Any) -> bytes:
    """Encodes input data in readiness for dispatch over wire.
    
    """
    # Recurse over tuples/lists.
    if isinstance(data, tuple):
        return tuple(map(encode, data))
    elif isinstance(data, list):
        return list(map(encode, data))

    # Skip non-custom types.
    if type(data) not in TYPESET:
        return data

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
