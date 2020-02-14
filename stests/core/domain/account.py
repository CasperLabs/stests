from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.domain.enums import AccountStatus
from stests.core.domain.enums import AccountType
from stests.core.domain.key_pair import PrivateKey
from stests.core.domain.meta import TypeMetadata
from stests.core.utils.domain import get_enum_field

    

@dataclass_json
@dataclass
class Account:
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

    # Associated metadata.
    meta: TypeMetadata

    @property
    def private_key_as_pem_filepath(self):
        return PrivateKey(self.private_key).as_pem_filepath



@dataclass_json
@dataclass
class AccountTransfer:
    """Encapsulates information pertaining to a CLX transfer between counterparties.
    
    """
    # Amount in motes that was transferred.
    amount: int

    # Asset being transferred.
    asset: str

    # Counter-party 1 account index.
    cp1_index: int

    # Counter-party 2 account index.
    cp2_index: int

    # Associated deploy hash.
    dhash: str

    # Flag indicating whether a refund is required.
    is_refundable: bool

    # Associated metadata.
    meta: TypeMetadata = TypeMetadata()