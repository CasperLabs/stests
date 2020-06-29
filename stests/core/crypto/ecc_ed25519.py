import typing

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from stests.core.crypto.enums import KeyEncoding
from stests.core.crypto.utils import get_bytes_from_pem_file



def get_key_pair() -> typing.Tuple[bytes, bytes]:
    """Returns an ED25519 key pair, each key is a 32 byte array.

    :param algo: Type of ECC algo to be used when generating key pair.
    :param encoding: Key pair encoding type.

    :returns : 2 member tuple: (private key, public key)
    
    """
    # Generate.
    sk = ed25519.Ed25519PrivateKey.generate()
    vk = sk.public_key()

    # Encode -> bytes.
    pvk = sk.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    pbk = vk.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    return pvk, pbk


def get_key_pair_from_pvk_pem_file(fpath: str) -> typing.Tuple[bytes, bytes]:
    """Returns an ED25519 key pair derived from a previously persisted PEM file.

    :param fpath: PEM file path.

    :returns : 2 member tuple: (private key, public key)
    
    """
    pvk = get_bytes_from_pem_file(fpath)
    sk = ed25519.Ed25519PrivateKey.from_private_bytes(pvk)
    vk = sk.public_key()
    pbk = vk.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    return pvk, pbk



def get_pvk_pem_from_bytes(pvk: bytes) -> bytes:
    """Returns ED25519 private key (pem) from bytes.
    
    """
    return ed25519.Ed25519PrivateKey.from_private_bytes(pvk).private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
