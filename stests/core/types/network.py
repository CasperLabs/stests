import enum
import typing
from dataclasses import dataclass
from dataclasses import field

from stests.core.types.enums import get_enum_field
from stests.core.types.enums import NetworkOperatorType
from stests.core.types.enums import NetworkStatus
from stests.core.types.enums import NetworkType
from stests.core.types.utils import Entity
from stests.core.utils import defaults



@dataclass
class Network(Entity):
    """A test network.
    
    """
    idx: int = 1
    nodeset: typing.List = field(default_factory=list)
    status: NetworkStatus = get_enum_field(NetworkStatus, NetworkStatus.NULL)
    typeof: NetworkType = get_enum_field(NetworkType, NetworkType.LOC)

    @property
    def key(self):
        """Returns network's key for identification purposes."""
        return Network.get_key(self.typeof, self.idx)


    @classmethod
    def get_key(cls, typeof: NetworkType, idx: int) -> str:
        """Returns network's key for identification purposes.
        
        """
        return f"{typeof.name}-{str(idx).zfill(3)}"


@dataclass
class NetworkEntity(Entity):
    """Base class for all entities associated with a network.
    
    """    
    network_idx: int = 1
    network_type: str =  get_enum_field(NetworkType, NetworkType.LOC)

    @property
    def network_key(self):
        """Returns associated network key."""
        return Network.get_key(self.network_type, self.network_idx)