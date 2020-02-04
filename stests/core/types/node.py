import enum
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime

from stests.core.types.account import Account
from stests.core.types.enums import AccountType

from stests.core.types.enums import get_enum_field
from stests.core.types.enums import NodeStatus
from stests.core.types.enums import NodeType
from stests.core.types.network import NetworkReference
from stests.core.types.network import NetworkType
from stests.core.types.utils import get_isodatetime_field
from stests.core.utils import defaults



@dataclass_json
@dataclass
class Node:
    """Represents a node within a target network.
    
    """
    # Bonding account associated with node.
    # TODO: review ?
    account: Account

    # Node's host address.
    host: str

    # Numerical index to distinguish between nodes, e.g. node-01, node-02 ...etc.
    index: int

    # Associated network reference information.
    network: NetworkReference

    # Node's external facing GRPC port.
    port: int

    # Current node status.
    status: NodeStatus = get_enum_field(NodeStatus)

    # Type of node in terms of it's degree of consensus participation.
    typeof: NodeType = get_enum_field(NodeType)
    
    # Standard time stamps.
    _ts_created: datetime = get_isodatetime_field(True)
    _ts_updated: datetime = get_isodatetime_field(True)

    @property
    def key(self):
        """Returns node's key for identification purposes."""
        return Node.get_key(self.index)

    @property
    def cache_key(self):
        return f"{self.network.name}.NODE:{str(self.index).zfill(4)}"

    @classmethod
    def get_key(cls, index: int):
        """Returns node's key for identification purposes.
        
        """
        return str(index).zfill(4)


    @staticmethod
    def create(
        account=None,
        host=defaults.NODE_HOST,
        index=defaults.NODE_INDEX,
        network=defaults.NETWORK_NAME,
        port=defaults.NODE_PORT,
        status=NodeStatus.NULL,
        typeof=NodeType[defaults.NODE_TYPE]
    ):
        """Factory method: leveraged in both live & test settings.
        
        """
        network = NetworkReference.create(network)

        return Node(account, host, index, network, port, status, typeof)

