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
    idx: int
    
    # Set of nodes that constitute the network.
    nodeset: typing.List
    
    # Current network status.
    status: NetworkStatus = get_enum_field(NetworkStatus)

    # Type of network, e.g. local, lrt, proof-of-concept ...etc.
    typeof: NetworkType = get_enum_field(NetworkType)

    # Standard time stamps.
    _ts_updated: datetime = get_isodatetime_field(True)
    _ts_created: datetime = get_isodatetime_field(True)

    @property
    def key(self):
        """Returns network's key for identification purposes."""
        return Network.get_key(self.typeof, self.idx)


    @classmethod
    def get_key(cls, typeof: NetworkType, idx: int) -> str:
        """Returns network's key for identification purposes.
        
        """
        return f"{typeof.name}-{str(idx).zfill(3)}"


    @staticmethod
    def create():
        """Factory: returns an instance for testing purposes.
        
        """
        return Network(
            idx=defaults.NETWORK_INDEX,
            nodeset=[],
            status=NetworkStatus.NULL,
            typeof=NetworkType[defaults.NETWORK_TYPE]
        )


@dataclass_json
@dataclass
class NetworkEntity:
    """Base class for all entities intimately associated with a network.
    
    """    
    # Numerical index to distinguish between multiple deployments of the same network type, e.g. lrt1, lrt2 ...etc.
    network_idx: int

    # Type of network, e.g. local, lrt, proof-of-concept ...etc.
    network_type: str =  get_enum_field(NetworkType)

    @property
    def network_key(self):
        """Returns associated network key."""
        return Network.get_key(self.network_type, self.network_idx)
