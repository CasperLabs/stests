
from stests.core.clx import crypto
from stests.core.types.core import KeyPair
from stests.core.types.account import Account
from stests.core.types.account import AccountTypeEnum



def create_user_account(index: int) -> Account:
    """Returns a DApp user account instance.
    
    """
    return _create_account(AccountTypeEnum.user, index)


def create_contract_account(index: int) -> Account:
    """Returns a DApp contract account instance.
    
    """
    return _create_account(AccountTypeEnum.contract, index)


def _create_account(typeof, index) -> Account:
    """Returns a DApp account instance.
    
    """
    pvk, pbk = crypto.create_key_pair(crypto.KeyEncodingEnum.hex)

    return Account(
        index=index,
        key_pair=KeyPair(private_key=pvk, public_key=pbk),
        typeof=typeof
        )
