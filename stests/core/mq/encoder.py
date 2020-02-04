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
    if isinstance(obj, dict):
        return {k: _encode(v) for k, v in obj.items()}
        
    if isinstance(obj, tuple):
        return tuple(map(_encode, obj))

    if isinstance(obj, list):
        return list(map(_encode, obj))

    if type(obj) in _encoder.TYPESET:
        return _encoder.encode(obj)

    return obj


def decode(data: bytes) -> MessageData:
    """Decodes data dispatched over wire.
    
    :param data: Bytestream to be decoded.
    :returns: Message data for further processing.

    """
    return _encoder.decode(json.loads(data.decode("utf-8")))
