import enum
import typing
from dataclasses import dataclass
from dataclasses import field

from stests.core.types.utils import Entity
from stests.core.types.utils import get_enum_field
from stests.core.utils import defaults



class NetworkStatus(enum.Flag):
    """Flag over set network states.
    
    """
    NULL = enum.auto()
    GENESIS = enum.auto()
    INITIALIZING = enum.auto()
    HEALTHY = enum.auto()
    DISTRESSED = enum.auto()
    DOWN = enum.auto()
    DE_INITIALIZING = enum.auto()


class NetworkOperatorType(enum.Enum):
    """Enumeration over set of network operator types.
    
    """
    LOCAL = enum.auto()
    INTERNAL = enum.auto()
    EXTERNAL = enum.auto()


class NetworkType(enum.Enum):
    """Enumeration over set of network types.
    
    """
    LOC = (NetworkOperatorType.LOCAL, "Developer tests")
    DEV = (NetworkOperatorType.INTERNAL, "Developer tests")
    LRT = (NetworkOperatorType.INTERNAL, "Long running tests")
    SYS = (NetworkOperatorType.INTERNAL, "Full system tests")
    STG = (NetworkOperatorType.INTERNAL, "Release staging")
    POC = (NetworkOperatorType.EXTERNAL, "Proof of concept")
    TEST = (NetworkOperatorType.EXTERNAL, "Chain candidate")
    MAIN = (NetworkOperatorType.EXTERNAL, "Main")


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
    def create(cls):
        """Factory: returns an instance for testing purposes.
        
        """
        return Network()


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