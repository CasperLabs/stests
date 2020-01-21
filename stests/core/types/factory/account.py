
from stests.core.clx import crypto
from stests.core.types.crypto import KeyPair
from stests.core.types.account import Account
from stests.core.types.account import AccountType



def create_account(typeof: AccountType, index: int) -> Account:
    """Returns a DApp account instance.
    
    """
    pvk, pbk = crypto.get_key_pair(crypto.KeyEncoding.BYTES)

    return Account(
        index=index,
        key_pair=KeyPair.create(pvk, pbk),
        typeof=typeof
        )
