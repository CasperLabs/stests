from dataclasses import dataclass
from enum import Enum

from dataclasses_json import dataclass_json

from stests.core.types.utils import get_enum_field



# Enum: Set of node states.
NodeStatusEnum = Enum("NodeStatusEnum", """
    NULL
    GENESIS
    INITIALIZING
    HEALTHY
    DISTRESSED
    DOWN
    DEINITIALIZING    
    """)


@dataclass_json
@dataclass
class Node():
    """Represents a node within a target network.
    
    """
    host: str
    port: int
    status: NodeStatusEnum = \
        get_enum_field(NodeStatusEnum, NodeStatusEnum.NULL)


# Set: supported domain types.
TYPESET = {
    Node,
}