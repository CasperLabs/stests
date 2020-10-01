from stests.core.crypto.account_id import get_account_id
from stests.core.crypto.enums import HashAlgorithm
from stests.core.crypto.enums import HashEncoding
from stests.core.crypto.enums import KeyAlgorithm
from stests.core.crypto.hashifier import get_hash



def get_account_hash(key_algo: KeyAlgorithm, public_key: str) -> str:
    """Returns an on-chain account hash.

    :param key_algo: Algorithm used to generate public key.
    :param public_key: Hexadecimal representation of an ECC verifying key.

    :returns: An on-chain account hash.

    """ 
    return get_hash(
        bytes.fromhex(get_account_id(key_algo, public_key)),
        algo=HashAlgorithm.BLAKE2B,
        encoding=HashEncoding.HEX,
    )
