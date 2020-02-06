from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.types.enums import get_enum_field
from stests.core.types.enums import AccountType
from stests.core.types.enums import NetworkType
from stests.core.utils import defaults



@dataclass_json
@dataclass
class NetworkIdentifier:
    """Information required to disambiguate between networks.
    
    """ 
    # Internal name of network, e.g. LRT-01
    name: str

    # External name of network, e.g. lrt1
    name_raw: str

    # Numerical index to distinguish between multiple deployments of the same network type, e.g. lrt1, lrt2 ...etc.
    index: int

    # Type of network, e.g. local, lrt, proof-of-concept ...etc.
    typeof: str =  get_enum_field(NetworkType)    


    @property
    def cache_key(self):
        """Returns key to be used when caching an instance."""
        return self.name


    @classmethod
    def create(cls, name_raw: str=defaults.NETWORK_NAME_RAW):
        """Factory method: leveraged in both live & test settings.

        """
        index = int(name_raw[3:])
        typeof = NetworkType[name_raw[:3].upper()]
        name = f"{typeof.name}-{str(index).zfill(2)}"

        return cls(name, name_raw, index, typeof)


@dataclass_json
@dataclass
class NodeIdentifier:
    """Information required to disambiguate between nodes.
    
    """ 
    # Associated network identifer.
    network: NetworkIdentifier

    # Node index.
    node: int


    @property
    def cache_key(self):
        """Returns key to be used when caching an instance."""
        return f"{self.network.cache_key}.NODE:{str(self.node).zfill(4)}"


    @classmethod
    def create(cls, network_name: str=defaults.NETWORK_NAME_RAW, node=defaults.NODE_INDEX):
        """Factory method: leveraged in both live & test settings.

        """
        network = NetworkIdentifier.create(network_name)

        return cls(network, node)


@dataclass_json
@dataclass
class GeneratorRunIdentifier:
    """Information required to disambiguate between generator runs.
    
    """
    # Associated network reference information.
    network: NetworkIdentifier
    
    # Numerical index to distinguish between multiple runs of the same generator.
    run: int

    # Type of generator, e.g. WG-100 ...etc.
    typeof: str

    @property
    def cache_key(self):
        """Returns key to be used when caching an instance."""
        return f"{self.network.cache_key}.{self.typeof}:R-{str(self.run).zfill(5)}"


    @classmethod
    def create(cls, run=defaults.GENERATOR_RUN, typeof="WG-XXX"):
        """Factory method: leveraged in both live & test settings.
        
        """
        return cls(run, typeof)


@dataclass_json
@dataclass
class AccountIdentifier:
    """Information required to disambiguate between accounts.
    
    """ 
    # Associated generator reference information.
    generator: GeneratorRunIdentifier

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