import dataclasses
import typing

from stests.core.types.infra.network import NetworkIdentifier



@dataclasses.dataclass
class ExecutionIdentifier:
    """Information required to disambiguate between generator runs.
    
    """
    # Associated network identifer.
    network: NetworkIdentifier
    
    # Numerical index to distinguish between multiple runs of the same generator.
    index: int

    # Type of generator, e.g. WG-100 ...etc.
    type: str
