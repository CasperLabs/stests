import json
import typing

from stests.core.mq.encoders.utils import encode as _encode
from stests.core.mq.encoders.utils import decode as _decode


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
