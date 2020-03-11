import dataclasses
import typing

from stests.core.domain.network import NetworkIdentifier



@dataclasses.dataclass
class RunIdentifier:
    """Information required to disambiguate between generator runs.
    
    """
    # Associated network identifer.
    network: NetworkIdentifier
    
    # Numerical index to distinguish between multiple runs of the same generator.
    index: int

    # Type of generator, e.g. WG-100 ...etc.
    type: str

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None
