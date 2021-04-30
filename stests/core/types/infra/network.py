import dataclasses
import typing

from stests.core.types.infra.enums import NetworkStatus
from stests.core.types.infra.enums import NetworkType



@dataclasses.dataclass
class Network:
    """A test network.

    """
    # Primary faucet associated with network.
    faucet: typing.Optional[typing.Any]

    # Count of bootstrap nodes associated with network.
    count_of_bootstrap_nodes: typing.Optional[int]

    # Count of genesis nodes associated with network.
    count_of_genesis_nodes: typing.Optional[int]

    # Name of chain associated with network.
    chain_name: typing.Optional[str]

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


@dataclasses.dataclass
class NetworkIdentifier:
    """Information required to disambiguate between networks.

    """
    # Internal name of network, e.g. LRT-01
    name: str

    @property
    def index(self) -> int:
        return int(self.name.split("-")[1])

    @property
    def type(self) -> NetworkType:
        return NetworkType[self.name.split("-")[0]]

    @property
    def key(self) -> str:
        return f"global.network:{self.name}"
