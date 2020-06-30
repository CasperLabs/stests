from stests.core.crypto.enums import HashAlgorithm
from stests.core.crypto.enums import HashEncoding
from stests.core.crypto.enums import KeyAlgorithm
from stests.core.crypto.hashifier import get_hash



def get_account_id(key_algo: KeyAlgorithm, public_key: str) -> str:
    """Returns an on-chain account identifier.

    :param key_algo: Algorithm used to generate public key.
    :param public_key: Hexadecimal representation of an ECC verifying key.

    :returns: An on-chain account identifier.

    """ 
    return get_hash(
        key_algo.name.encode("UTF-8") + b"\x00" + bytes.fromhex(public_key),
        algo=HashAlgorithm.BLAKE2B,
        encoding=HashEncoding.HEX,   
    )
