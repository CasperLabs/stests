from dataclasses import dataclass

from stests.core.domain.account import Account
from stests.core.domain.enums import NodeStatus
from stests.core.domain.enums import NodeType
from stests.core.utils.domain import *



@dataclass
class Node(Entity):
    """Represents a node within a target network.
    
    """
    # Bonding account associated with node.
    account: Account

    # Node's host address.
    host: str

    # Numerical index to distinguish between nodes, e.g. node-01, node-02 ...etc.
    index: int

    # Network with which node is associated.
    network: str

    # Node's external facing GRPC port.
    port: int

    # Current node status.
    status: NodeStatus = get_enum_field(NodeStatus)

    # Type of node in terms of it's degree of consensus participation.
    typeof: NodeType = get_enum_field(NodeType)
    
    # Type key of associated object used in serialisation scenarios.
    _type_key: str = None

    # Timestamp: create.
    _ts_created: datetime = get_isodatetime_field(True)

    # Timestamp: update.
    _ts_updated: datetime = get_isodatetime_field(True)

    # Universally unique identifier.
    _uid: str = get_uuid_field(True) 

    @property
    def label(self):
        return f"{self.network}:{self.index}"
