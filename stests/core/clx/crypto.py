import typing
from enum import Enum

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from stests.core.types import KeyEncoding



def get_key_pair(encoding: KeyEncoding = KeyEncoding.BYTES) -> typing.Tuple[str, str]:
    """Returns an ED25519 key pair, each key is a 32 byte array.

    :rtype: 2 member tuple: (private key, public key)
    
    """
    # Guard.
    if not isinstance(encoding, KeyEncoding):
        raise ValueError(f"Unsupported key encoding: {encoding}")

    # Create new key pair.
    pvk = ed25519.Ed25519PrivateKey.generate()
    pbk = pvk.public_key()

    # PEM.
    if encoding == KeyEncoding.PEM:
        return \
            pvk.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ), \
            pbk.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )  

    # Encode -> bytes.
    pvk = pvk.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    pbk = pbk.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    # HEX.
    if encoding == KeyEncoding.HEX:
        return pvk.hex(), pbk.hex()

    # BYTES.
    return pvk, pbk
