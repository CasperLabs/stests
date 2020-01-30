import enum
import random
import typing
from dataclasses import dataclass

from stests.core.types.key_pair import KeyPair
from stests.core.types.utils import Entity
from stests.core.types.utils import get_enum_field
from stests.core.utils import defaults



class AccountStatus(enum.Flag):
    """Flag over set account states.
    
    """
    NEW = enum.auto()
    FUNDING = enum.auto()
    FUNDED = enum.auto()
    ACTIVE = enum.auto()


class AccountType(enum.Enum):
    """Enumeration over set of account types.
    
    """
    CONTRACT = enum.auto()
    FAUCET = enum.auto()
    USER = enum.auto()
    BOND = enum.auto()


@dataclass
class Account(Entity):
    """An account that maps to an address upon target chain.
    
    """
    idx: int = 1
    key_pair: KeyPair = KeyPair.create()
    status: AccountStatus = get_enum_field(AccountStatus, AccountStatus.NEW)
    typeof: AccountType = get_enum_field(AccountType)


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
