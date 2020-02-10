import inspect
import json
import typing

from stests.core.utils import encoder as _encoder



# Represents contents of a Message object as a dict.
MessageData = typing.Dict[str, typing.Any]


def encode(data: MessageData) -> bytes:
    """Encodes input data in readiness for dispatch over wire.

    :param data: Message data to be dispatched over wire.
    :returns: Bytestream for dispatch.
    
    """
    return json.dumps(_encoder.encode(data), separators=(",", ":")).encode("utf-8")


def decode(data: bytes) -> MessageData:
    """Decodes data dispatched over wire.
    
    :param data: Bytestream to be decoded.
    :returns: Message data for further processing.

    """
    return _encoder.decode(json.loads(data.decode("utf-8")))
