from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.domain.enums import AccountType
from stests.core.domain.enums import NetworkType
from stests.core.utils.domain import get_enum_field



@dataclass_json
@dataclass
class NetworkIdentifier:
    """Information required to disambiguate between networks.
    
    """ 
    # Internal name of network, e.g. LRT-01
    name: str   

    @property
    def index(self) -> int:
        return int(self.name.split("-")[1])

    @property
    def typeof(self) -> NetworkType:
        return NetworkType[self.name.split("-")[0]]



@dataclass_json
@dataclass
class NodeIdentifier:
    """Information required to disambiguate between nodes.
    
    """ 
    # Associated network identifer.
    network: NetworkIdentifier

    # Node index.
    index: int


@dataclass_json
@dataclass
class RunIdentifier:
    """Information required to disambiguate between generator runs.
    
    """
    # Associated network reference information.
    network: NetworkIdentifier
    
    # Numerical index to distinguish between multiple runs of the same generator.
    run: int

    # Type of generator, e.g. WG-100 ...etc.
    typeof: str


@dataclass_json
@dataclass
class AccountIdentifier:
    """Information required to disambiguate between accounts.
    
    """ 
    # Associated generator reference information.
    generator: RunIdentifier

    # Numerical index to distinguish between accounts within same context.
    index: int

    # Associated network reference information.
    network: NetworkIdentifier

    # Type of account, e.g. USER | FAUCET | BOND | CONTRACT.
    typeof: AccountType = get_enum_field(AccountType)


    @property
    def cache_key(self):
        """Returns key to be used when caching an instance."""
        key = self.network.cache_key
        if self.generator:
            key += f".{self.generator.cache_key}"
        return key + f":ACCOUNTS:{self.typeof.name}:{str(self.index).zfill(6)}"


# Domain identifiers.
IDENTIFIER_SET = {
    NetworkIdentifier,
    NodeIdentifier,
    RunIdentifier,
}
