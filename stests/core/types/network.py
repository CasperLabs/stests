from dataclasses import dataclass
from enum import Enum
from enum import Flag
from typing import List

from dataclasses_json import dataclass_json

from stests.core.types.node import Node
from stests.core.types.utils import get_enum_field



# Enum: Set of network lifetimes.
NetworkLifetime = Enum("NetworkLifetime", [
    "SINGLETON",
    "REPEAT",
    "SEMI_PERSISTENT",
    "PERSISTENT"
    ])


# Enum: Set of network operators.
NetworkOperator = Enum("NetworkOperator", [
    "LOCAL",
    "INTERNAL",
    "EXTERNAL"
    ])


# Enum: Set of network states.
NetworkStatus = Flag("NetworkStatus", [
    "NULL",
    "GENESIS",
    "INITIALIZING",
    "HEALTHY",
    "DISTRESSED",
    "DOWN",
    "DE_INITIALIZING"
    ])


@dataclass_json
@dataclass
class Network():
    """Represents a network that is being tested.
    
    """
    name: str
    nodeset: List[Node]
    lifetime: NetworkLifetime = \
        get_enum_field(NetworkLifetime, NetworkLifetime.REPEAT)
    operator: NetworkOperator = \
        get_enum_field(NetworkOperator, NetworkOperator.LOCAL)
    status: NetworkStatus = \
        get_enum_field(NetworkStatus, NetworkStatus.NULL)


    @staticmethod
    def create():
        """Factory: returns an instance for testing purposes.
        
        """
        return Network("DEV-LOC-01", [])


# Set: supported domain types.
CLASSES = {
    Network,
}

# Set: supported domain enums.
ENUMS = {
    NetworkLifetime,
    NetworkOperator,
    NetworkStatus
}