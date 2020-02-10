from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.domain.account import Account
from stests.core.domain.enums import NetworkStatus
from stests.core.domain.enums import NetworkType
from stests.core.utils.domain import get_enum_field
from stests.core.utils.domain import TypeMetadata



@dataclass_json
@dataclass
class Network:
    """A test network.
    
    """
    # Primary faucet associated with network.
    faucet: Account

    # Numerical index to distinguish between multiple deployments of the same network type, e.g. lrt1, lrt2 ...etc.
    index: int
    
    # Network's name, e.g. LRT-01.
    name: str

    # Network's raw name, e.g. lrt1.
    name_raw: str
    
    # Current network status.
    status: NetworkStatus = get_enum_field(NetworkStatus)

    # Type of network, e.g. local, lrt, proof-of-concept ...etc.
    typeof: NetworkType = get_enum_field(NetworkType)

    # Associated metadata.
    meta: TypeMetadata = TypeMetadata()