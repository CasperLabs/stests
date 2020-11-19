from stests.core.crypto.enums import KeyAlgorithm



# Map: key algorithm to key prefix.
_KEY_ALGO_PREFIX = {
    KeyAlgorithm.ED25519: "01",
    KeyAlgorithm.SECP256K1: "02",
}


def get_account_key(key_algo: KeyAlgorithm, public_key: str) -> str:
    """Returns an on-chain account identifier.

    :param key_algo: Algorithm used to generate public key.
    :param public_key: Hexadecimal representation of an ECC verifying key.

    :returns: An on-chain account identifier.

    """ 
    try:
        _KEY_ALGO_PREFIX[key_algo]
    except KeyError:
        raise KeyError(f"Unsupported key type: {key_algo}")

    return f"{_KEY_ALGO_PREFIX[key_algo]}{public_key}"
