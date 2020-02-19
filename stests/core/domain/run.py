import typing
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.domain.meta import TypeMetadata



@dataclass_json
@dataclass
class RunContext:
    """Contextual information associated with each generator run.
    
    """
    # Associated run arguments.
    args: typing.Any

    # Associated network.
    network: str

    # Associated node index.
    node_index: int

    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: int

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str

    # Associated metadata.
    meta: TypeMetadata = TypeMetadata()

    @property
    def keypath(self):
        return [
            self.network,
            self.run_type,
            f"R-{str(self.run_index).zfill(3)}"            
        ]


@dataclass_json
@dataclass
class RunEvent:
    """Event information associated with a generator run.
    
    """
    # Event name.
    event: str

    # Associated network.
    network: str

    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: int

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str

    # Moment in time when event occurred.
    timestamp: int

    # Associated metadata.
    meta: TypeMetadata = TypeMetadata()
