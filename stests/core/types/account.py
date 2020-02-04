import enum
import random
import typing
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime

from stests.core.types.enums import AccountStatus
from stests.core.types.enums import AccountType
from stests.core.types.generator import GeneratorReference
from stests.core.types.network import NetworkReference
from stests.core.types.enums import get_enum_field
from stests.core.types.key_pair import KeyPair
from stests.core.types.utils import get_isodatetime_field
from stests.core.utils import defaults




@dataclass_json
@dataclass
class Account:
    """An account that maps to an address upon target chain.
    
    """
    # Associated generator reference information.
    generator: GeneratorReference

    # Numerical index to distinguish between accounts within same context.
    index: int

    # Associated cryptographic key pair for signing/verification/authentication.
    key_pair: KeyPair

    # Associated network reference information.
    network: NetworkReference

    # Current account status.
    status: AccountStatus = get_enum_field(AccountStatus)

    # Type of account, e.g. USER | FAUCET | BOND | CONTRACT.
    typeof: AccountType = get_enum_field(AccountType)

    # Standard time stamps.
    _ts_created: datetime = get_isodatetime_field(True)
    _ts_updated: datetime = get_isodatetime_field(True)


    @property
    def cache_key(self) -> str:
        """Returns key to be used when caching an instance."""
        key = self.network.cache_key
        if self.generator:
            key += f".{self.generator.cache_key}"
        return key + f":ACCOUNTS:{self.typeof.name}:{str(self.index).zfill(6)}"


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
        network = network if isinstance(network, NetworkReference) else NetworkReference.create(network)
        typeof = typeof or random.choice(list(AccountType))

        return Account(generator, index, key_pair, network, status, typeof)
