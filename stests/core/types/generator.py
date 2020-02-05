import datetime
import uuid
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.types.network import NetworkReference
from stests.core.utils import defaults



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


    @classmethod
    def create(cls, run=defaults.GENERATOR_RUN, typeof="WG-XXX"):
        """Factory method: leveraged in both live & test settings.
        
        """
        return GeneratorReference(run, typeof)


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
        return f"{self.network.cache_key}.{self.get_reference().cache_key}:CTX"


    def get_reference(self):
        """Returns information required to disambiguate between generator runs."""
        return GeneratorReference(self.run, self.typeof)


    @classmethod
    def create(
        cls,
        network=defaults.NETWORK_NAME,
        node=defaults.NODE_INDEX,
        run=defaults.GENERATOR_RUN,
        typeof="WG-XXX"
        ):
        """Factory method: leveraged in both live & test settings.
        
        """
        return GeneratorContext(
            NetworkReference.create(network),
            node,
            run,
            typeof
            )