import typing
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.utils.domain import TypeMetadata



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
