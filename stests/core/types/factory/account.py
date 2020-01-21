
from stests.core.clx import crypto
from stests.core.types.core import KeyPair
from stests.core.types.account import Account
from stests.core.types.account import AccountType



def create_account(typeof: AccountType, index: int) -> Account:
    """Returns a DApp account instance.
    
    """
    (pvk_bytes, pvk_hex, pvk_pem), (pbk_bytes, pbk_hex, pbk_pem) = crypto.get_account_keys()

    return Account(
        index=index,
        key_pair=KeyPair(private_key=pvk_hex, public_key=pbk_hex),
        typeof=typeof
        )
