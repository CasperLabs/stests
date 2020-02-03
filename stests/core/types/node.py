import enum
from dataclasses import dataclass

from stests.core.types.account import Account
from stests.core.types.enums import AccountType

from stests.core.types.enums import get_enum_field
from stests.core.types.enums import NodeStatus
from stests.core.types.enums import NodeType
from stests.core.types.network import NetworkEntity
from stests.core.types.network import NetworkType
from stests.core.types.utils import Entity
from stests.core.utils import defaults



@dataclass
class Node(NetworkEntity):
    """Represents a node within a target network.
    
    """
    # Bonding account associated with node.
    # TODO: review ?
    account: Account

    # Node's host address.
    host: str

    # Numerical index to distinguish between nodes, e.g. node-01, node-02 ...etc.
    idx: int

    # Node's external facing GRPC port.
    port: int

    # Current node status.
    status: NodeStatus = get_enum_field(NodeStatus)

    # Type of node in terms of it's degree of consensus participation.
    typeof: NodeType = get_enum_field(NodeType)
    
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
        return Node(
            account=Account.create(AccountType.BOND),
            host=defaults.NODE_HOST,
            idx=defaults.NODE_INDEX,
            port=defaults.NODE_PORT,
            status=NodeStatus.NULL,
            typeof=NodeType[defaults.NODE_TYPE],
            # TODO: review            
            network_idx=defaults.NETWORK_INDEX,
            network_type=NetworkType[defaults.NETWORK_TYPE]
        )
