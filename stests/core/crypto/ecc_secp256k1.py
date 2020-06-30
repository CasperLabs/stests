import typing

import ecdsa

from stests.core.crypto.enums import KeyEncoding



# Curve of interest.
CURVE = ecdsa.SECP256k1

# Use uncompressed public keys.
UNCOMPRESSED = "uncompressed"


def get_key_pair() -> typing.Tuple[bytes, bytes]:
    """Returns an SECP256K1 key pair, each key is a 32 byte array.

    :returns : 2 member tuple: (private key, public key)
    
    """    
    return _get_key_pair_from_sk(ecdsa.SigningKey.generate(curve=CURVE))


def get_key_pair_from_pvk_pem_file(fpath: str) -> typing.Tuple[bytes, bytes]:
    """Returns an SECP256K1 key pair derived from a previously persisted PEM file.

    :param fpath: PEM file path.

    :returns : 2 member tuple: (private key, public key)
    
    """
    as_pem = _get_bytes_from_pem_file(fpath)
    as_pem = as_pem.decode("UTF-8")

    return _get_key_pair_from_sk(ecdsa.SigningKey.from_pem(as_pem))


def get_pvk_pem_from_bytes(pvk: bytes) -> bytes:
    """Returns SECP256K1 private key (pem) from bytes.
    
    """
    return ecdsa.SigningKey.from_string(pvk, curve=CURVE).to_pem()


def _get_bytes_from_pem_file(fpath: str) -> bytes:
    """Returns bytes from a pem file.
    
    """
    with open(fpath, "rb") as f:
        return f.read()


def _get_key_pair_from_sk(sk: ecdsa.SigningKey) -> typing.Tuple[bytes, bytes]:
    """Returns key pair from a signing key.
    
    """
    return sk.to_string(), \
           sk.verifying_key.to_string(UNCOMPRESSED)
