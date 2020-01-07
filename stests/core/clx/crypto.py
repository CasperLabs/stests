from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from enum import Enum



# Enum: set of supported key encodings.
KeyEncoding = Enum("KeyEncoding", [
    "BYTES",
    "HEX"
    ])


def create_key_pair(encoding: KeyEncoding = KeyEncoding.BYTES):
    """Returns an ED25519 key pair, each key is a 32 byte array.

    :rtype: 2 member tuple: (private key, public key)
    
    """
    # Create new private key.
    pvk = ed25519.Ed25519PrivateKey.generate()

    # Set byte array representations.
    pbk = pvk.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    pvk = pvk.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Return Convert to hex if requested.
    if encoding == KeyEncoding.BYTES:
        return pvk, pbk
    if encoding == KeyEncoding.HEX:
        return pvk.hex(), pbk.hex()

    raise TypeError(f"{encoding} key pair encoding is unsupported")
