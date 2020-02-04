import enum
import typing
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from dataclasses import field
from datetime import datetime

from stests.core.types.enums import get_enum_field
from stests.core.types.enums import NetworkOperatorType
from stests.core.types.enums import NetworkStatus
from stests.core.types.enums import NetworkType
from stests.core.types.utils import get_isodatetime_field
from stests.core.utils import defaults



@dataclass_json
@dataclass
class Network:
    """A test network.
    
    """
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

    # Standard time stamps.
    _ts_created: datetime = get_isodatetime_field(True)
    _ts_updated: datetime = get_isodatetime_field(True)

    @property
    def cache_key(self):
        """Returns key to be used when caching an instance."""
        return f"{self.typeof.name}-{str(self.index).zfill(2)}"

    @property
    def key(self):
        """Returns network's key for identification purposes."""
        return Network.get_key(self.typeof, self.index)


    @classmethod
    def get_key(cls, typeof: NetworkType, index: int) -> str:
        """Returns network's key for identification purposes.
        
        """
        return f"{typeof.name}-{str(index).zfill(2)}"


    @staticmethod
    def create(
        index=defaults.NETWORK_INDEX,
        nodeset=[],
        status=NetworkStatus.NULL,
        typeof=NetworkType[defaults.NETWORK_TYPE]
        ):
        """Factory: returns an instance for testing purposes.
        
        """
        name = f"{typeof.name}-{str(index).zfill(2)}"
        name_raw = f"{typeof.name.lower()}{index}"

        return Network(index, name, name_raw, nodeset, status, typeof)


@dataclass_json
@dataclass
class NetworkReference:
    """Information used to disambiguate between networks.
    
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

        return NetworkReference(name, name_raw, index, typeof)
