from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum
from enum import Flag

from stests.core.types.account import Account
from stests.core.types.account import AccountType
from stests.core.types.utils import get_enum_field
from stests.core.utils import defaults



# Enum: Set of node states.
NodeStatus = Flag("NodeStatus", [
    "NULL",
    "GENESIS",
    "INITIALIZING",
    "HEALTHY",
    "DISTRESSED",
    "DOWN",
    "DEINITIALIZING"    
    ])


# Enum: Set of node types.
NodeType = Enum("NodeType", [
    "FULL",
    "READ_ONLY"
    ])


@dataclass_json
@dataclass
class NodeMetadata():
    """Metadata associated with test node.
    
    """
    typeof: NodeType = \
        get_enum_field(NodeType, NodeType.FULL)


    @classmethod
    def create(cls):
        """Factory: returns an instance for testing purposes.
        
        """
        return NodeMetadata()


@dataclass_json
@dataclass
class Node():
    """Represents a node within a target network.
    
    """
    host: str = defaults.NODE_HOST
    port: int = defaults.NODE_PORT
    network_id: str = defaults.NETWORK_ID
    operator: Account = None
    metadata: NodeMetadata = NodeMetadata()
    status: NodeStatus = \
        get_enum_field(NodeStatus, NodeStatus.NULL)


    @staticmethod
    def create():
        """Factory: returns an instance for testing purposes.
        
        """
        return Node(
            operator=Account.create(AccountType.VALIDATOR)
            )
