import dataclasses
import typing
from datetime import datetime

from stests.core.types.chain.account import Account
from stests.core.types.infra.enums import NodeEventType
from stests.core.types.infra.enums import NodeStatus
from stests.core.types.infra.enums import NodeType
from stests.core.types.infra.network import NetworkIdentifier



@dataclasses.dataclass
class Node:
    """Encpasulates information pertaining to a node within a target network.
    
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
    
    @property
    def address(self):
        return f"{self.host}:{self.port}"

    @property
    def label_index(self):
        return f"N-{str(self.index).zfill(4)}"

    @property
    def is_operational(self):
        return self.status in (NodeStatus.HEALTHY, NodeStatus.DISTRESSED)

    @property
    def label(self):
        return f"{self.network}:{self.index}"



@dataclasses.dataclass
class NodeEventLock:
    """Encpasulates information used to lock processing a node event.
    
    """
    # Hash of block associated with event.
    block_hash: str

    # Hash of deploy associated with event.
    deploy_hash: str

    # Node specific event identifier.
    event_id: int

    # Moment in time when event was streamed.
    event_ts: datetime

    # Node event type.
    event_type: NodeEventType

    # Associated network.
    network: str

    # Node from which deploy was streamed.
    node: int

    @property
    def label_event_id(self):
        return f"E-{str(self.event_id).zfill(9)}"

    @property
    def label_event_type(self):
        return self.event_type.name

    @property
    def label_node_index(self):
        return f"N-{str(self.node).zfill(4)}"


@dataclasses.dataclass
class NodeIdentifier:
    """Encpasulates information required to disambiguate between nodes.
    
    """ 
    # Associated network identifer.
    network: NetworkIdentifier

    # Node index.
    index: int
 
    @property
    def label_index(self):
        return f"N-{str(self.index).zfill(4)}"

    @property
    def label(self):
        return f"{self.network.name}:{self.label_index}"


@dataclasses.dataclass
class NodeMonitoringLock:
    """Encpasulates information used to lock monitoring of a node.
    
    """
    # Numerical index to distinguish between nodes upon the same network.
    index: int

    # Associated network.
    network: str

    # Numerical index to distinguish between multiple locks.
    lock_index: int

    @property
    def label_index(self):
        return f"N-{str(self.index).zfill(4)}"



