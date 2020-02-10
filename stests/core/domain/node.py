from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.domain.account import Account
from stests.core.domain.enums import NodeStatus
from stests.core.domain.enums import NodeType
from stests.core.utils.domain import get_enum_field
from stests.core.utils.domain import TypeMetadata



@dataclass_json
@dataclass
class Node:
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

    # Associated metadata.
    meta: TypeMetadata = TypeMetadata()
    
    @property
    def key(self) -> str:
        """Returns node's key for identification purposes."""
        return str(self.index).zfill(4)
