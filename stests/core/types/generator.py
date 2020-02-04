import datetime
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.types.network import NetworkReference
from stests.core.types.utils import get_isodatetime_field



@dataclass_json
@dataclass
class GeneratorReference:
    """Encpasulates enough information to identify a generator run.
    
    """
    # Numerical index to distinguish between multiple runs of the same generator.
    run: int

    # Type of generator, e.g. WG-100 ...etc.
    typeof: str

    @property
    def cache_key(self):
        """Returns key to be used when caching an instance."""
        return f"{self.typeof}:R-{str(self.run).zfill(5)}"


@dataclass_json
@dataclass
class GeneratorContext:
    """Information collected eact time a generator is executed.
    
    """
    # Associated network reference information.
    network: NetworkReference

    # Associated node reference information.
    node: int

    # Numerical index to distinguish between multiple runs of the same generator.
    run: int

    # Type of generator being executed.
    typeof: str

    @property
    def cache_key(self):
        """Returns key to be used when caching an instance."""
        return f"{self.network.cache_key}:{self.get_reference().cache_key}"


    def get_reference(self):
        """Returns information required to disambiguate between generator runs."""
        return GeneratorReference(self.run, self.typeof)

