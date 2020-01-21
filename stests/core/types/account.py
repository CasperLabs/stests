import random
import typing
from dataclasses import dataclass
from enum import Enum
from enum import Flag

from dataclasses_json import dataclass_json

from stests.core.types.core import KeyPair
from stests.core.types.utils import get_enum_field



# Flag: Set of account states.
AccountStatus = Flag("AccountStatus", [
    "NEW",
    "FUNDING",
    "FUNDED",
    "ACTIVE"
    ])


# Enum: Set of account types.
AccountType = Enum("AccountType", [
    "CONTRACT",
    "USER"
    ])


@dataclass_json
@dataclass
class Account:
    """A DApp account that maps to an address upon target network.
    
    """
    index: int
    key_pair: KeyPair
    status: AccountStatus = \
        get_enum_field(AccountStatus, AccountStatus.NEW)
    typeof: AccountType = \
        get_enum_field(AccountType)


    @property
    def short_type(self) -> str:
        """Returns short type name.
        
        """
        return str(self.typeof).split('.')[-1]


    @staticmethod
    def create():
        """Factory: returns an instance for testing purposes.
        
        """
        return Account(0, KeyPair.create(), typeof=random.choice(list(AccountType)))
