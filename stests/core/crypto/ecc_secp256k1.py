import typing

import ecdsa

from stests.core.crypto.enums import KeyEncoding
from stests.core.crypto.utils import get_bytes_from_pem_file



# Curve of interest.
CURVE = ecdsa.SECP256k1

# Use uncompressed public keys.
UNCOMPRESSED = "uncompressed"


def get_key_pair() -> typing.Tuple[bytes, bytes]:
    """Returns an SECP256K1 key pair, each key is a 32 byte array.

    :returns : 2 member tuple: (private key, public key)
    
    """    
    # Generate.
    sk = ecdsa.SigningKey.generate(curve=CURVE)
    vk = sk.verifying_key

    # Encode -> bytes.
    pvk = sk.to_string()
    pbk = vk.to_string(UNCOMPRESSED)

    return pvk, pbk


def get_key_pair_from_pvk_pem_file(fpath: str) -> typing.Tuple[bytes, bytes]:
    """Returns an SECP256K1 key pair derived from a previously persisted PEM file.

    :param fpath: PEM file path.

    :returns : 2 member tuple: (private key, public key)
    
    """
    pvk = get_bytes_from_pem_file(fpath)
    sk = ecdsa.SigningKey.from_string(pvk, curve=CURVE)
    vk = sk.verifying_key

    # Encode -> bytes.
    pbk = vk.to_string(UNCOMPRESSED)

    return pvk, pbk


def get_pvk_pem_from_bytes(pvk: bytes) -> bytes:
    """Returns SECP256K1 private key (pem) from bytes.
    
    """
    return ecdsa.SigningKey.from_string(pvk, curve=CURVE).to_pem()
