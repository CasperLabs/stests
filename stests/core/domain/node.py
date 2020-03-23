import dataclasses
import typing
from datetime import datetime

from stests.core.domain.account import Account
from stests.core.domain.enums import NodeStatus
from stests.core.domain.enums import NodeType
from stests.core.domain.network import NetworkIdentifier
from stests.core.utils.dataclasses import get_timestamp_field



@dataclasses.dataclass
class Node:
    """Represents a node within a target network.
    
    """
    # Bonding account associated with node.
    account: typing.Optional[Account]

    # Node's host address.
    host: str

    # Numerical index to distinguish between nodes, e.g. node-01, node-02 ...etc.
    index: int

    # Network with which node is associated.
    network: str

    # Node's external facing GRPC port.
    port: int

    # Current node status.
    status: NodeStatus

    # Type of node in terms of it's degree of consensus participation.
    typeof: NodeType
    
    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    # Timestamp: create.
    _ts_created: datetime = get_timestamp_field()

    @property
    def index_label(self):
        return str(self.index).zfill(3)

    @property
    def is_operational(self):
        return self.status in (NodeStatus.HEALTHY, NodeStatus.DISTRESSED)

    @property
    def label(self):
        return f"{self.network}:{self.index}"


@dataclasses.dataclass
class NodeIdentifier:
    """Information required to disambiguate between nodes.
    
    """ 
    # Associated network identifer.
    network: NetworkIdentifier

    # Node index.
    index: int
 
     # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None


@dataclasses.dataclass
class NodeStreamLock:
    """Execution lock information - stream.
    
    """
    # Associated network.
    network: str

    # Numerical index to distinguish between nodees upon the same network.
    node_index: int

    # Numerical index to distinguish between multiple locks.
    lock_index: int

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None
