from dataclasses import dataclass
from enum import Enum

from dataclasses_json import dataclass_json

from stests.core.types.core import KeyPair
from stests.core.types.utils import get_enum_field



# Enum: Set of account states.
AccountStatusEnum = Enum("AccountStatusEnum", "new funding funded active")


# Enum: Set of account types.
AccountTypeEnum = Enum("AccountTypeEnum", "contract user")


@dataclass_json
@dataclass
class Account:
    """A DApp account that maps to an address upon target network.
    
    """
    index: int
    key_pair: KeyPair
    status: AccountStatusEnum = \
        get_enum_field(AccountStatusEnum, AccountStatusEnum.new)
    typeof: AccountTypeEnum = \
        get_enum_field(AccountTypeEnum)


    @property
    def identifiers(self):
        """Returns set of identifiers that can be used to disambiguate accounts.
        
        """
        return {
            self.index,
            self.key_pair.private_key,
            self.key_pair.public_key
            }

    
    @property
    def short_type(self) -> str:
        """Returns short type name.
        
        """
        return str(self.typeof).split('.')[-1]


# Set: supported domain types.
TYPESET = {
    Account,
    AccountStatusEnum,
    AccountTypeEnum
}
