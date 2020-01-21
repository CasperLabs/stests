import typing

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from enum import Enum



# Enum: set of supported key encodings.
KeyEncoding = Enum("KeyEncoding", [
    "BYTES",
    "HEX",
    "PEM"
    ])


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


def get_account_keys():
    """Returns an ED25519 key pair encoded in byte, hex & PEM formats.

    :rtype: 2 member tuple: ((bytes, str, str), (bytes, str, str))
    
    """    
    # Create new key pair.
    pvk = ed25519.Ed25519PrivateKey.generate()
    pbk = pvk.public_key()

    # Encode private key -> bytes.
    pvk_bytes = pvk.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Encode private key -> hex.
    pvk_hex = pvk_bytes.hex()

    # Encode private key -> PEM.
    pvk_pem = pvk.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Encode public key -> bytes.
    pbk_bytes = pbk.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    # Encode public key -> hex.
    pbk_hex = pbk_bytes.hex()

    # Encode public key -> PEM.
    pbk_pem = pbk.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return \
        (pvk_bytes, pvk_hex, pvk_pem), \
        (pbk_bytes, pbk_hex, pbk_pem)
