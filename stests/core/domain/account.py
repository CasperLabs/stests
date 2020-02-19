from dataclasses import dataclass

from stests.core.domain.enums import AccountStatus
from stests.core.domain.enums import AccountType
from stests.core.domain.key_pair import PrivateKey
from stests.core.utils.domain import *



@dataclass
class Account(Entity):
    """A non-designated account that maps to an address upon target chain.
    
    """
    # Numerical index to distinguish between multiple accounts within same run.
    index: int

    # Hexadecimal representation of private key used primarily in signing scenarios.
    private_key: str

    # Hexadecimal representation of public key used primarily in identity & verification scenarios.
    public_key: str

    # Current account status.
    status: AccountStatus = get_enum_field(AccountStatus)

    # Type of account, e.g. USER | FAUCET | BOND | CONTRACT.
    typeof: AccountType = get_enum_field(AccountType)

    # Type key of associated object used in serialisation scenarios.
    _type_key: str = None

    # Timestamp: create.
    _ts_created: datetime = get_isodatetime_field(True)

    # Timestamp: update.
    _ts_updated: datetime = get_isodatetime_field(True)

    # Universally unique identifier.
    _uid: str = get_uuid_field(True) 

    @property
    def private_key_as_pem_filepath(self):
        return PrivateKey(self.private_key).as_pem_filepath
