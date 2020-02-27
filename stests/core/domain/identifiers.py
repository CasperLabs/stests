import typing
from dataclasses import dataclass

from stests.core.domain.enums import NetworkType



@dataclass
class NetworkIdentifier:
    """Information required to disambiguate between networks.
    
    """ 
    # Internal name of network, e.g. LRT-01
    name: str   

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Union[None, str] = None

    @property
    def index(self) -> int:
        return int(self.name.split("-")[1])

    @property
    def type(self) -> NetworkType:
        return NetworkType[self.name.split("-")[0]]

    @property
    def key(self) -> str:
        return f"global.network:{self.name}"


@dataclass
class NodeIdentifier:
    """Information required to disambiguate between nodes.
    
    """ 
    # Associated network identifer.
    network: NetworkIdentifier

    # Node index.
    index: int
 
     # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Union[None, str] = None


@dataclass
class RunIdentifier:
    """Information required to disambiguate between generator runs.
    
    """
    # Associated network identifer.
    network: NetworkIdentifier
    
    # Numerical index to distinguish between multiple runs of the same generator.
    index: int

    # Type of generator, e.g. WG-100 ...etc.
    type: str

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Union[None, str] = None


@dataclass
class AccountIdentifier:
    """Information required to disambiguate between accounts.
    
    """ 
    # Numerical index to distinguish between accounts within same context.
    index: int

    # Associated run identifier.
    run: RunIdentifier

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Union[None, str] = None

    @property
    def network_id(self) -> NetworkIdentifier:
        return this.run.network
