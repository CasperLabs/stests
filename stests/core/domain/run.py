import typing
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.utils.domain import TypeMetadata
from stests.core.domain import NetworkIdentifier
from stests.core.domain import NodeIdentifier



@dataclass_json
@dataclass
class RunContext:
    """Contextual information associated with each generator run.
    
    """
    # Associated run arguments.
    args: typing.Any

    # Numerical index to distinguish between multiple runs of the same generator.
    index: int

    # Associated network reference.
    network: str

    # Associated node reference.
    node: int

    # Type of generator, e.g. WG-100 ...etc.
    typeof: str

    # Associated metadata.
    meta: TypeMetadata = TypeMetadata()

    @property
    def network_id(self) -> NetworkIdentifier:
        return NetworkIdentifier(self.network)

    @property
    def node_id(self) -> NodeIdentifier:
        return NodeIdentifier(self.network_id, self.node)

    @property
    def run_index(self) -> int:
        return self.index

    @property
    def run_type(self) -> str:
        return self.typeof


@dataclass_json
@dataclass
class RunEvent:
    """Event information associated with a generator run.
    
    """
    # Event name.
    event: str

    # Associated network reference.
    network: str

    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: int

    # Type of generator, e.g. WG-100 ...etc.
    run_typeof: str

    # Moment in time when event occurred.
    timestamp: int

    # Associated metadata.
    meta: TypeMetadata = TypeMetadata()
