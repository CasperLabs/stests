import inspect
import typing

from stests.core.utils import encoder as _encoder



# Represents contents of a Message object as a dict.
MessageData = typing.Dict[str, typing.Any]


def encode(data: MessageData) -> bytes:
    """Encodes input data in readiness for dispatch over wire.

    :param data: Message data to be dispatched over wire.
    :returns: Bytestream for dispatch.
    
    """
    return _encoder.as_json(data)


def decode(data: bytes) -> MessageData:
    """Decodes data dispatched over wire.
    
    :param data: Bytestream to be decoded.
    :returns: Message data for further processing.

    """
    return _encoder.from_json(data.decode("utf-8"))


def initialise():
    """Initialises encoder to ensure all types are registered.

    """
    _encoder.initialise()
