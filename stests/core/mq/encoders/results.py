import json

from stests.core.mq.encoders.utils import encode as _encode



def encode(data: tuple) -> bytes:
    """Encodes actor results in readiness for persistence.

    :param data: Tuple of actor results to be persisted.
    :returns: Bytestream for persistence.
    
    """
    data = _encode(data)

    return json.dumps(data, separators=(",", ":")).encode("utf-8")


def decode(data: bytes) -> tuple:
    """Decodes previously stored actor results in readiness for downstream processing.

    :param data: Previously persisted bytestream of actor results.
    :returns: Decodes actor results.
    
    """
    raise NotImplementedError("Not required at this time")
