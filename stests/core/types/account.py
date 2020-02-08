import random
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime

from stests.core.types.enums import AccountStatus
from stests.core.types.enums import AccountType
from stests.core.types.enums import get_enum_field
from stests.core.types.identifiers import AccountIdentifier
from stests.core.types.identifiers import GeneratorRunIdentifier
from stests.core.types.identifiers import NetworkIdentifier
from stests.core.types.key_pair import KeyPair
from stests.core.types.utils import get_isodatetime_field
from stests.core.types.utils import get_uuid_field
from stests.core.utils import defaults

from stests.core.types.meta import TypeMetadata



@dataclass_json
@dataclass
class Account:
    """An account that maps to an address upon target chain.
    
    """
    # Numerical index to distinguish between accounts within same context.
    index: int

    # Associated cryptographic key pair for signing/verification/authentication.
    key_pair: KeyPair

    # Current account status.
    status: AccountStatus = get_enum_field(AccountStatus)

    # Type of account, e.g. USER | FAUCET | BOND | CONTRACT.
    typeof: AccountType = get_enum_field(AccountType)

    # Associated metadata.
    meta: TypeMetadata


    @property
    def cache_key(self) -> str:
        """Returns key to be used when caching an instance."""
        key = self.generator.cache_key if self.generator else self.network.cache_key

        return key + f":data:ACCOUNTS:{self.typeof.name}:{str(self.index).zfill(6)}"


    def get_identifier(self) -> AccountIdentifier:
        """Returns information required for identification purposes.
        
        """
        return AccountIdentifier(self.generator, self.index, self.network, self.typeof)


    @classmethod
    def create(
        cls,
        generator=None,
        index=defaults.ACCOUNT_INDEX,
        key_pair=None,
        network=defaults.NETWORK_NAME,
        status=AccountStatus.NEW,
        typeof=None
        ):
        """Factory method: leveraged in both live & test settings.
        
        """
        key_pair=key_pair or KeyPair.create()
        network = network if isinstance(network, NetworkIdentifier) else NetworkIdentifier.create(network)
        typeof = typeof or random.choice(list(AccountType))

        return cls(generator, index, key_pair, network, status, typeof)

