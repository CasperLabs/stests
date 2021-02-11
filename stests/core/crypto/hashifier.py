import typing

from stests.core.crypto import hashifier_blake2b as blake2b
from stests.core.crypto.enums import HashAlgorithm
from stests.core.crypto.enums import HashEncoding



# Map: Hash Algo Type -> Hash Algo Implementation.
ALGOS = {
    HashAlgorithm.BLAKE2B: blake2b,
}

ENCODERS = {
    HashEncoding.BYTES: lambda x: x,
    HashEncoding.HEX: lambda x: x.hex(),
}


def get_hash(
    data: bytes,
    size: int = 32,
    algo: HashAlgorithm = HashAlgorithm.BLAKE2B,
    encoding: HashEncoding = HashEncoding.BYTES,
    ) -> typing.Union[bytes, str]:
    """Maps input to a blake2b hash.
    
    :param data: Data to be hashed.
    :param size: Desired hashing output length.
    :param algo: Type of hashing algo to apply.
    :param encoding: Hash output encoding type.

    :returns: Encoded hash of input data.

    """ 
    return ENCODERS[encoding](ALGOS[algo].get_hash(data, size))
