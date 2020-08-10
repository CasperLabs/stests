from stests.core.crypto.enums import HashAlgorithm
from stests.core.crypto.enums import HashEncoding
from stests.core.crypto.enums import KeyAlgorithm
from stests.core.crypto.hashifier import get_hash



# Seperator to be applied when setting data to be passed to hashifier.
_SEPERATOR = b"\x00"


def get_account_id(key_algo: KeyAlgorithm, public_key: str) -> str:
    """Returns an on-chain account identifier.

    :param key_algo: Algorithm used to generate public key.
    :param public_key: Hexadecimal representation of an ECC verifying key.

    :returns: An on-chain account identifier.

    """ 
    return get_hash(
        key_algo.name.encode("UTF-8") + _SEPERATOR + bytes.fromhex(public_key),
        algo=HashAlgorithm.BLAKE2B,
        encoding=HashEncoding.HEX,   
    )
