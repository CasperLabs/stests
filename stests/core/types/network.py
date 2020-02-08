import typing
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime

from stests.core.types.account import Account
from stests.core.types.enums import get_enum_field
from stests.core.types.enums import NetworkStatus
from stests.core.types.enums import NetworkType
from stests.core.types.identifiers import NetworkIdentifier
from stests.core.types.utils import get_isodatetime_field
from stests.core.types.utils import get_uuid_field
from stests.core.utils import defaults


from stests.core.types.meta import TypeMetadata



@dataclass_json
@dataclass
class Network:
    """A test network.
    
    """
    # Bonding account associated with node.
    # TODO: review ?
    faucet: Account

    # Numerical index to distinguish between multiple deployments of the same network type, e.g. lrt1, lrt2 ...etc.
    index: int
    
    # Network's common name, e.g. LRT-001.
    name: str

    # Network's raw name, e.g. lrt1.
    name_raw: str

    # Set of nodes that constitute the network.
    nodeset: typing.List
    
    # Current network status.
    status: NetworkStatus = get_enum_field(NetworkStatus)

    # Type of network, e.g. local, lrt, proof-of-concept ...etc.
    typeof: NetworkType = get_enum_field(NetworkType)

    # Standard fields.
    _ts_created: datetime = get_isodatetime_field(True)
    _ts_updated: datetime = get_isodatetime_field(True)
    _uid: str = get_uuid_field(True) 


    @property
    def cache_key(self):
        """Returns key to be used when caching an instance."""
        return f"{self.typeof.name}-{str(self.index).zfill(2)}"


    @property
    def key(self):
        """Returns network's key for identification purposes."""
        return Network.get_key(self.typeof, self.index)


    def get_identifier(self) -> NetworkIdentifier:
        """Returns information required for identification purposes.
        
        """
        return NetworkIdentifier(self.name, self.name_raw, self.index, self.typeof)


    @classmethod
    def get_key(cls, typeof: NetworkType, index: int) -> str:
        """Returns network's key for identification purposes.
        
        """
        return f"{typeof.name}-{str(index).zfill(2)}"


    @classmethod
    def create(
        cls,
        faucet=None,
        index=defaults.NETWORK_INDEX,
        nodeset=[],
        status=NetworkStatus.NULL,
        typeof=NetworkType[defaults.NETWORK_TYPE]
        ):
        """Factory: returns an instance for testing purposes.
        
        """
        name = f"{typeof.name}-{str(index).zfill(2)}"
        name_raw = f"{typeof.name.lower()}{index}"

        return cls(faucet, index, name, name_raw, nodeset, status, typeof)
