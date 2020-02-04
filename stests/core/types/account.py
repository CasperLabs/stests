import enum
import random
import typing
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime

from stests.core.types.enums import AccountStatus
from stests.core.types.enums import AccountType
from stests.core.types.enums import get_enum_field
from stests.core.types.key_pair import KeyPair
from stests.core.types.utils import get_isodatetime_field
from stests.core.utils import defaults



@dataclass_json
@dataclass
class Account:
    """An account that maps to an address upon target chain.
    
    """
    # Numerical index to distinguish between multiple deployments of the same network type, e.g. lrt1, lrt2 ...etc.
    idx: int

    # Key pair with which to interact with target network.
    key_pair: KeyPair

    # Status of account in terms of it's network participation.
    status: AccountStatus = get_enum_field(AccountStatus)

    # Type of account, e.g. USER | FAUCET | BOND | CONTRACT.
    typeof: AccountType = get_enum_field(AccountType)

    # Standard time stamps.
    _ts_created: datetime = get_isodatetime_field(True)
    _ts_updated: datetime = get_isodatetime_field(True)


    @property
    def short_type(self) -> str:
        """Returns short type name.
        
        """
        return str(self.typeof).split('.')[-1]


    @staticmethod
    def create(idx=1, key_pair=None, typeof=None, status=AccountStatus.NEW):
        """Factory: returns an instance for testing purposes.
        
        """
        return Account(
            idx=idx,
            key_pair=key_pair or KeyPair.create(),
            status=status,
            typeof=typeof or random.choice(list(AccountType))
            )
