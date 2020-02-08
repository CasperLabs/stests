from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.domain.enums import AccountStatus
from stests.core.domain.enums import AccountType
from stests.core.domain.enums import get_enum_field
from stests.core.domain.meta import TypeMetadata



@dataclass_json
@dataclass
class Account:
    """An account that maps to an address upon target chain.
    
    """
    # Private key used primarily in signing scenarios.
    private_key: str

    # Public key used primarily in identity & verification scenarios.
    public_key: str

    # Current account status.
    status: AccountStatus = get_enum_field(AccountStatus)

    # Type of account, e.g. USER | FAUCET | BOND | CONTRACT.
    typeof: AccountType = get_enum_field(AccountType)

    # Associated metadata.
    meta: TypeMetadata



@dataclass_json
@dataclass
class UserAccount(Account):
    """A network user account.
    
    """
    # Numerical index to distinguish between accounts within same context.
    index: int
