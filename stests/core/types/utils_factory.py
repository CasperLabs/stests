
from stests.core import clx
from stests.core.types.key_pair import KeyPair
from stests.core.types.account import Account
from stests.core.types.account import AccountType
from stests.core.utils import logger



def create_account(typeof: AccountType, index: int, network_id: str) -> Account:
    """Returns a DApp account instance.
    
    """
    pvk, pbk = clx.get_key_pair(clx.KeyEncoding.BYTES)
    account = Account(
        index=index,
        key_pair=KeyPair.create(pvk, pbk),
        network_id=network_id,
        typeof=typeof
        )

    logger.log(f"TYPES :: new-account :: {typeof} :: {account.key_pair.public_key.as_hex}")
    
    return account