import enum
import random
import typing
from dataclasses import dataclass

from stests.core.types.enums import AccountStatus
from stests.core.types.enums import AccountType
from stests.core.types.enums import get_enum_field
from stests.core.types.key_pair import KeyPair
from stests.core.types.utils import Entity
from stests.core.utils import defaults



@dataclass
class Account(Entity):
    """An account that maps to an address upon target chain.
    
    """
    idx: int = 1
    key_pair: KeyPair = KeyPair.create()
    status: AccountStatus = get_enum_field(AccountStatus, AccountStatus.NEW)
    typeof: AccountType = get_enum_field(AccountType, AccountType.USER)


    @property
    def short_type(self) -> str:
        """Returns short type name.
        
        """
        return str(self.typeof).split('.')[-1]


    @staticmethod
    def create(typeof=None):
        """Factory: returns an instance for testing purposes.
        
        """
        return Account(
            key_pair=KeyPair.create(),
            typeof=typeof or random.choice(list(AccountType))
            )
