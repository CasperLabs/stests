import enum
import random
import typing
from dataclasses import dataclass
from datetime import datetime

from stests.core.types.enums import AccountStatus
from stests.core.types.enums import AccountType
from stests.core.types.enums import get_enum_field
from stests.core.types.key_pair import KeyPair
from stests.core.types.utils import Entity
from stests.core.types.utils import get_isodatetime_field
from stests.core.utils import defaults



@dataclass
class Account(Entity):
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

    _ts_created: datetime = get_isodatetime_field()


    @property
    def short_type(self) -> str:
        """Returns short type name.
        
        """
        return str(self.typeof).split('.')[-1]


    @staticmethod
    def create(typeof=None):
        """Factory: returns an instance for testing purposes.
        
        """
        print(888)
        return Account(
            idx=1,
            key_pair=KeyPair.create(),
            status=AccountStatus.NEW,
            typeof=typeof or random.choice(list(AccountType)),
            _ts_created=datetime.now()
            )
