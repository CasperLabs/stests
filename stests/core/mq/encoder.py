import json
import typing

from stests.core.types import TYPESET
from stests.core.utils.execution import ExecutionContext



# Extend typeset.
TYPESET = TYPESET | { ExecutionContext, }

# Set typemap.
# Map: domain type keys -> domain type.  
TYPEMAP = {f"{i.__module__}.{i.__name__}": i for i in TYPESET}

# Represents contents of a Message object as a dict.
MessageData = typing.Dict[str, typing.Any]


def encode(data: MessageData) -> bytes:
    """Encodes input data in readiness for dispatch over wire.

    :param data: Message data to be dispatched over wire.
    :returns: Bytestream for dispatch.
    
    """
    # Encode outgoing domain objects.
    data['args'] = _encode(data['args'])

    return json.dumps(data, separators=(",", ":")).encode("utf-8")


def _encode(data: typing.Any) -> bytes:
    """Encodes input data in readiness for dispatch over wire.
    
    """
    # Recurse over tuples/lists.
    if isinstance(data, tuple):
        return tuple(map(_encode, data))
    elif isinstance(data, list):
        return list(map(_encode, data))

    # Skip non-custom types.
    if type(data) not in TYPESET:
        return data

    # Convert custom types to dictionary.
    obj = data.to_dict()

    # Append type info for downstream round-trip.
    obj['_type'] = f"{data.__module__}.{data.__class__.__name__}"

    return obj


def decode(data: bytes) -> MessageData:
    """Decodes data dispatched over wire.
    
    :param data: Bytestream to be decoded.
    :returns: Message data for further processing.

    """
    # Decode raw json.
    data = json.loads(data.decode("utf-8"))
    
    # Decode incoming domain objects.
    if 'args' in data:
        data['args'] = _decode(data['args'])

    return data


def _decode(data: bytes) -> typing.Any:
    """Decodes data dispatched over wire.
    
    """
    # Recurse over tuples/lists.
    if isinstance(data, tuple):
        return tuple(map(_decode, data))
    elif isinstance(data, list):
        return list(map(_decode, data))

    # Skip all except dictionaries with injected type field.
    if not isinstance(data, dict) or '_type' not in data:
        return data

    # Get type to be instantiated.
    cls = TYPEMAP[data['_type']]
    
    # Return type instance hydrated from incoming data.
    return cls.from_dict(data)
