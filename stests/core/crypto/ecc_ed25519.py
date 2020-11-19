import base64
import typing

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from stests.core.crypto.enums import KeyEncoding



def get_key_pair() -> typing.Tuple[bytes, bytes]:
    """Returns an ED25519 key pair, each key is a 32 byte array.

    :param algo: Type of ECC algo to be used when generating key pair.
    :param encoding: Key pair encoding type.

    :returns : 2 member tuple: (private key, public key)
    
    """
    return _get_key_pair_from_sk(ed25519.Ed25519PrivateKey.generate())


def get_key_pair_from_pvk_b64(pvk_b64: str) -> typing.Tuple[bytes, bytes]:
    """Returns an ED25519 key pair derived from a previously base 64 private key.

    :param pvk_b64: Base64 encoded private key.

    :returns : 2 member tuple: (private key, public key)
    
    """
    return _get_key_pair_from_sk(
        ed25519.Ed25519PrivateKey.from_private_bytes(
            base64.b64decode(pvk_b64)
            )
        )


def get_key_pair_from_pvk_pem_file(fpath: str) -> typing.Tuple[bytes, bytes]:
    """Returns an ED25519 key pair derived from a previously persisted PEM file.

    :param fpath: PEM file path.

    :returns : 2 member tuple: (private key, public key)
    
    """
    return _get_key_pair_from_sk(
        ed25519.Ed25519PrivateKey.from_private_bytes(
            _get_bytes_from_pem_file(fpath)
            )
        )


def get_key_pair_from_seed(seed: bytes) -> typing.Tuple[bytes, bytes]:
    """Returns an ED25519 key pair derived from a seed.

    :param seed: A seed used as input to deterministic key pair generation.

    :returns : 2 member tuple: (private key, public key)
    
    """
    sk = ed25519.Ed25519PrivateKey.from_private_bytes(seed)

    return _get_key_pair_from_sk(sk)


def get_pvk_pem_from_bytes(pvk: bytes) -> bytes:
    """Returns ED25519 private key (pem) from bytes.
    
    """
    return ed25519.Ed25519PrivateKey.from_private_bytes(pvk).private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )


def _get_bytes_from_pem_file(fpath: str) -> bytes:
    """Returns bytes from a pem file.
    
    """
    with open(fpath, 'r') as fstream:
        as_pem = fstream.readlines()
    as_b64 = [l for l in as_pem if l and not l.startswith("-----")][0].strip()
    as_bytes = base64.b64decode(as_b64)

    return len(as_bytes) % 32 == 0 and as_bytes[:32] or as_bytes[-32:]


def _get_key_pair_from_sk(sk: ed25519.Ed25519PrivateKey) -> typing.Tuple[bytes, bytes]:
    """Returns key pair from a signing key.
    
    """
    pk = sk.public_key()

    return \
        sk.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        ), \
        pk.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
