import tempfile
import typing

from stests.core.crypto import ecc_ed25519 as ed25519
from stests.core.crypto import ecc_secp256k1 as secp256k1
from stests.core.crypto.enums import KeyAlgorithm
from stests.core.crypto.enums import KeyEncoding



# Map: ECC Algo Type -> ECC Algo Implementation.
ALGOS = {
    KeyAlgorithm.ED25519: ed25519,
    KeyAlgorithm.SECP256K1: secp256k1,
}


def get_key_algo(key: str) -> KeyAlgorithm:
    """Returns algorithm of an account key.

    :param key: An account key from which an algorithm can be derived.

    :returns: A supported key algorithm.

    """
    if key.startswith('01'):
        return KeyAlgorithm.ED25519
    if key.startswith('02'):
        return KeyAlgorithm.SECP256K1

    raise ValueError("Unsupported key type.")


def get_key_pair(algo: KeyAlgorithm, encoding: KeyEncoding = KeyEncoding.BYTES) -> typing.Tuple[bytes, bytes]:
    """Returns an ECC key pair, each key is a 32 byte array.

    :param algo: Type of ECC algo to be used when generating key pair.
    :param encoding: Key pair encoding type.

    :returns : 2 member tuple: (private key, public key)
    
    """
    pvk, pbk = ALGOS[algo].get_key_pair()

    return (pvk.hex(), pbk.hex()) if encoding == KeyEncoding.HEX else (pvk, pbk)


def get_key_pair_from_pvk_b64(pvk_b64: str, algo: KeyAlgorithm, encoding: KeyEncoding = KeyEncoding.BYTES):
    """Returns an ECC key pair derived from a previously base 64 private key.

    :param pvk_b64: Base64 encoded private key.
    :param algo: Type of ECC algo used to generate private key.
    :param encoding: Key pair encoding type.

    :returns : 2 member tuple: (private key, public key)
    
    """
    pvk, pbk = ALGOS[algo].get_key_pair_from_pvk_b64(pvk_b64)

    return (pvk.hex(), pbk.hex()) if encoding == KeyEncoding.HEX else (pvk, pbk)


def get_key_pair_from_pvk_pem_file(fpath: str, algo: KeyAlgorithm, encoding: KeyEncoding = KeyEncoding.BYTES):
    """Returns an ECC key pair derived from a previously persisted PEM file.

    :param fpath: PEM file path.
    :param algo: Type of ECC algo used to generate private key.
    :param encoding: Key pair encoding type.

    :returns : 2 member tuple: (private key, public key)
    
    """
    pvk, pbk = ALGOS[algo].get_key_pair_from_pvk_pem_file(fpath)

    return (pvk.hex(), pbk.hex()) if encoding == KeyEncoding.HEX else (pvk, pbk)


def get_key_pair_from_seed(seed: bytes, algo: KeyAlgorithm, encoding: KeyEncoding = KeyEncoding.BYTES):
    """Returns an ED25519 key pair derived from a seed.

    :param seed: Seed from which a key pair will be generated.
    :param algo: Type of ECC algo used to generate private key.
    :param encoding: Key pair encoding type.

    :returns : 2 member tuple: (private key, public key)
    
    """
    pvk, pbk = ALGOS[algo].get_key_pair_from_seed(seed)

    return (pvk.hex(), pbk.hex()) if encoding == KeyEncoding.HEX else (pvk, pbk)


def get_pvk_pem_from_bytes(pvk: bytes, algo: KeyAlgorithm) -> bytes:
    """Returns an ECC private key in PEM format.

    :param pvk: Private key.
    :param algo: Type of ECC algo used to generate private key.

    :returns : Private key in PEM format.
    
    """
    return ALGOS[algo].get_pvk_pem_from_bytes(pvk)


def get_pvk_pem_file_from_bytes(pvk: bytes, algo: KeyAlgorithm) -> bytes:
    """Returns path to a file containing an ECC private key in PEM format.

    :param pvk: Private key.
    :param algo: Type of ECC algo used to generate private key.

    :returns : Private key in PEM format.
    
    """
    with tempfile.NamedTemporaryFile("wb", delete=False) as temp_file:
        with open(temp_file.name, "wb") as fstream:
            fstream.write(get_pvk_pem_from_bytes(pvk, algo))

        return temp_file.name
