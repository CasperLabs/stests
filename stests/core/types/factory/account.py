
from stests.core.clx import crypto
from stests.core.types.core import KeyPair
from stests.core.types.account import Account
from stests.core.types.account import AccountType



def create_user_account(index: int) -> Account:
    """Returns a DApp user account instance.
    
    """
    return _create_account(AccountType.USER, index)


def create_contract_account(index: int) -> Account:
    """Returns a DApp contract account instance.
    
    """
    return _create_account(AccountType.CONTRACT, index)


def _create_account(typeof, index) -> Account:
    """Returns a DApp account instance.
    
    """
    pvk, pbk = crypto.create_key_pair(crypto.KeyEncoding.HEX)

    return Account(
        index=index,
        key_pair=KeyPair(private_key=pvk, public_key=pbk),
        typeof=typeof
        )
