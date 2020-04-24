import base64
import enum
import typing

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519



class KeyEncoding(enum.Enum):
    """Enumeration over set of key encodings.
    
    """
    BYTES = enum.auto()
    HEX = enum.auto()
    PEM = enum.auto()


def generate_key_pair(encoding: KeyEncoding = KeyEncoding.BYTES) -> typing.Tuple[str, str]:
    """Returns an ED25519 key pair, each key is a 32 byte array.

    :rtype: 2 member tuple: (private key, public key)
    
    """
    # Guard.
    if not isinstance(encoding, KeyEncoding):
        raise ValueError(f"Unsupported key encoding: {encoding}")

    # Instantiate.
    pvk = ed25519.Ed25519PrivateKey.generate()

    # Encode.
    return _get_key_pair(pvk, encoding)


def get_key_pair_from_pvk_bytes(pvk_bytes, encoding: KeyEncoding = KeyEncoding.BYTES) -> typing.Tuple[str, str]:
    """Returns a key pair derived from an existing private key.
    
    """
    pvk = ed25519.Ed25519PrivateKey.from_private_bytes(pvk_bytes)

    return _get_key_pair(pvk, encoding)


def get_key_pair_from_pvk_pem_file(fpath, encoding: KeyEncoding = KeyEncoding.BYTES) -> typing.Tuple[str, str]:
    """Returns a key pair derived from an existing private key.
    
    """
    pvk_bytes = get_pvk_bytes_from_pem_file(fpath)

    return get_key_pair_from_pvk_bytes(pvk_bytes, encoding)


def get_pbk_bytes_from_pem_file(fpath):
    """Returns public key (bytes) pulled from a PEM file.
    
    """
    return _get_bytes_from_pem_file(fpath)


def get_pbk_hex_from_pem_file(fpath):
    """Returns public key (hex) pulled from a PEM file.
    
    """
    as_bytes = get_pbk_bytes_from_pem_file(fpath)

    return as_bytes.hex()


def get_pbk_pem_from_bytes(pbk_bytes):
    """Returns public key (pem) from bytes.
    
    """
    return ed25519.Ed25519PublicKey.from_public_bytes(pbk_bytes).public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )


def get_pvk_bytes_from_pem_file(fpath):
    """Returns private key (bytes) pulled from a PEM file.
    
    """
    return _get_bytes_from_pem_file(fpath)


def get_pvk_hex_from_pem_file(fpath):
    """Returns private key (hex) pulled from a PEM file.
    
    """
    as_bytes = get_pvk_bytes_from_pem_file(fpath)

    return as_bytes.hex()


def get_pvk_pem_from_bytes(pvk_bytes):
    """Returns private key (pem) from bytes.
    
    """
    return ed25519.Ed25519PrivateKey.from_private_bytes(pvk_bytes).private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )


def _get_bytes_from_pem_file(fpath):
    """Returns bytes from a pem file.
    
    """
    with open(fpath, 'r') as fstream:
        as_pem = fstream.readlines()
    as_b64 = [l for l in as_pem if l and not l.startswith("-----")][0].strip()
    as_bytes = base64.b64decode(as_b64)

    return len(as_bytes) % 32 == 0 and as_bytes[:32] or as_bytes[-32:]


def _get_key_pair(pvk: ed25519.Ed25519PrivateKey, encoding: KeyEncoding) -> typing.Tuple[str, str]:
    """Maps private key to an encoded key pair.
    
    """
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