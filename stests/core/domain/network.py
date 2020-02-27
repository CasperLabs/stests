import typing
from dataclasses import dataclass

from stests.core.domain.account import Account
from stests.core.domain.enums import NetworkStatus
from stests.core.domain.enums import NetworkType
from stests.core.utils.domain import *



@dataclass
class Network(Entity):
    """A test network.
    
    """
    # Primary faucet associated with network.
    faucet: typing.Optional[Account]

    # Numerical index to distinguish between multiple deployments of the same network type, e.g. lrt1, lrt2 ...etc.
    index: int
    
    # Network's name, e.g. LRT-01.
    name: str

    # Network's raw name, e.g. lrt1.
    name_raw: str
    
    # Current network status.
    status: NetworkStatus

    # Type of network, e.g. local, lrt, proof-of-concept ...etc.
    typeof: NetworkType

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    # Timestamp: create.
    _ts_created: datetime = get_isodatetime_field(True)

    # Timestamp: update.
    _ts_updated: datetime = get_isodatetime_field(True)

    # Universally unique identifier.
    _uid: str = get_uuid_field(True) 
