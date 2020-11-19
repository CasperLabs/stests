from stests.core.crypto.account_key import get_account_key
from stests.core.crypto.ecc import get_key_algo
from stests.core.crypto.enums import HashAlgorithm
from stests.core.crypto.enums import HashEncoding
from stests.core.crypto.enums import KeyAlgorithm
from stests.core.crypto.hashifier import get_hash



def get_account_hash(account_key: str) -> str:
    """Returns an on-chain account hash as derived from an account identifier.

    :param account_key: An on-chain account identifier.

    :returns: An on-chain account hash.

    """ 
    return get_account_hash_from_public_key(
        get_key_algo(account_key),
        account_key[2:]
        )


def get_account_hash_from_public_key(key_algo: KeyAlgorithm, public_key: str) -> str:
    """Returns an on-chain account hash derived from a public key.

    :param key_algo: Algorithm used to generate public key.
    :param public_key: Hexadecimal representation of an ECC verifying key.

    :returns: An on-chain account hash.

    """ 
    as_bytes = \
        bytes(key_algo.name.lower(), "utf-8") + \
        bytearray(1) + \
        bytes.fromhex(public_key)

    return get_hash(as_bytes, 32, HashAlgorithm.BLAKE2B, HashEncoding.HEX)
