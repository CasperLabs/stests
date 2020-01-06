from dataclasses import dataclass
from enum import Enum
from typing import List

from dataclasses_json import dataclass_json

from stests.core.types.node import Node
from stests.core.types.utils import get_enum_field


# Enum: Set of network states.
NetworkStatusEnum = Enum("NetworkStatusEnum", """
    NULL
    GENESIS
    INITIALIZING
    HEALTHY
    DISTRESSED
    DOWN
    DE_INITIALIZING    
    """)


# Enum: Set of network lifetimes.
NetworkLifetimeEnum = Enum("NetworkLifetimeEnum", """
    SINGLETON
    REPEAT
    SEMI_PERSISTENT
    PERSISTENT
    """)


# Enum: Set of network operators.
NetworkOperatorEnum = Enum("NetworkOperatorEnum", """
    LOCAL
    INTERNAL
    EXTERNAL
    """)


@dataclass_json
@dataclass
class Network():
    """Represents a network that is being tested.
    
    """
    name: str
    nodeset: List[Node]
    lifetime: NetworkLifetimeEnum = \
        get_enum_field(NetworkLifetimeEnum, NetworkLifetimeEnum.REPEAT)
    operator: NetworkOperatorEnum = \
        get_enum_field(NetworkOperatorEnum, NetworkOperatorEnum.LOCAL)
    status: NetworkStatusEnum = \
        get_enum_field(NetworkStatusEnum, NetworkStatusEnum.NULL)


# Set: supported domain types.
TYPESET = {
    Network,
}