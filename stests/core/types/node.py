import enum
from dataclasses import dataclass

from stests.core.types.account import Account
from stests.core.types.account import AccountType
from stests.core.types.network import NetworkEntity
from stests.core.types.utils import Entity
from stests.core.types.utils import get_enum_field
from stests.core.utils import defaults



class NodeStatus(enum.Flag):
    """Flag over set node states.
    
    """
    NULL = enum.auto()
    GENESIS = enum.auto()
    INITIALIZING = enum.auto()
    HEALTHY = enum.auto()
    DISTRESSED = enum.auto()
    DOWN = enum.auto()
    DE_INITIALIZING = enum.auto()


class NodeType(enum.Enum):
    """Enumeration over set of node types.
    
    """
    FULL = enum.auto()
    READ_ONLY = enum.auto()


@dataclass
class Node(NetworkEntity):
    """Represents a node within a target network.
    
    """
    idx: int = 1
    status: NodeStatus = get_enum_field(NodeStatus, NodeStatus.NULL)
    typeof: NodeType = get_enum_field(NodeType, NodeType.FULL)
    host: str = defaults.NODE_HOST
    port: int = defaults.NODE_PORT
    account: Account = Account.create(AccountType.BOND)

    @property
    def key(self):
        """Returns node's key for identification purposes."""
        return Node.get_key(self.idx)


    @classmethod
    def get_key(cls, idx: int):
        """Returns node's key for identification purposes.
        
        """
        return str(idx).zfill(4)


    @staticmethod
    def create():
        """Factory: returns an instance for testing purposes.
        
        """
        return Node()