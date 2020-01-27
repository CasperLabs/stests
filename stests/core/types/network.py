from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum
from enum import Flag
from typing import List

from stests.core.types.node import Node
from stests.core.types.utils import get_enum_field



# Enum: Set of network lifetimes.
NetworkLifetime = Enum("NetworkLifetime", [
    "SINGLETON",
    "REPEAT",
    "SEMI_PERSISTENT",
    "PERSISTENT"
    ])


# Enum: Set of network operator types.
NetworkOperatorType = Enum("NetworkOperatorType", [
    "LOCAL",
    "INTERNAL",
    "HYBRID",
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
class NetworkMetadata():
    """Metadata associated with test network.
    
    """
    lifetime: NetworkLifetime = \
        get_enum_field(NetworkLifetime, NetworkLifetime.REPEAT)
    operatorType: NetworkOperatorType = \
        get_enum_field(NetworkOperatorType, NetworkOperatorType.LOCAL)


    @classmethod
    def create(cls):
        """Factory: returns an instance for testing purposes.
        
        """
        return NetworkMetadata()


@dataclass_json
@dataclass
class Network():
    """A test network.
    
    """
    name: str
    nodeset: List[Node]
    metadata: NetworkMetadata = NetworkMetadata()
    status: NetworkStatus = \
        get_enum_field(NetworkStatus, NetworkStatus.NULL)


    @classmethod
    def create(cls):
        """Factory: returns an instance for testing purposes.
        
        """
        return Network("DEV-LOC-01", [
            Node.create(),
        ])
