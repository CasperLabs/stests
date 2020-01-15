
from stests.core.clx import crypto
from stests.core.types.core import KeyPair
from stests.core.types.account import Account
from stests.core.types.account import AccountType



def create_account(typeof: AccountType, index: int) -> Account:
    """Returns a DApp account instance.
    
    """
    pvk, pbk = crypto.create_key_pair(crypto.KeyEncoding.HEX)

    return Account(
        index=index,
        key_pair=KeyPair(private_key=pvk, public_key=pbk),
        typeof=typeof
        )
