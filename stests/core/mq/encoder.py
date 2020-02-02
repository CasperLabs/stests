import json
import typing

from stests.core.utils import encoder as _encoder
from stests.core.utils.encoder import decode as _decode



# Represents contents of a Message object as a dict.
MessageData = typing.Dict[str, typing.Any]


def encode(data: MessageData) -> bytes:
    """Encodes input data in readiness for dispatch over wire.

    :param data: Message data to be dispatched over wire.
    :returns: Bytestream for dispatch.
    
    """
    return json.dumps(_encode(data), separators=(",", ":")).encode("utf-8")


def _encode(obj: typing.Any) -> typing.Any:
    """Encode message data.
    
    """
    # Parse dictionaries.
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, dict):
                obj[k] = _encode(v)
            elif isinstance(v, tuple):
                obj[k] = tuple(map(_encode, v))
            elif isinstance(v, list):
                obj[k] = list(map(_encode, v))        
            else:
                obj[k] = _encode(v)

    # Encode stests types.
    if type(obj) in _encoder.TYPESET:
        return _encoder.encode(obj)
        
    return obj


def decode(data: bytes) -> MessageData:
    """Decodes data dispatched over wire.
    
    :param data: Bytestream to be decoded.
    :returns: Message data for further processing.

    """
    # Decode raw json.
    data = json.loads(data.decode("utf-8"))

    # Decode any incoming workflow arguments.
    try:
        data['args']
    except KeyError:
        pass
    else:
        data['args'] = _encoder.decode(data['args'])

    return data
