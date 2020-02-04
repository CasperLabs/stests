import datetime
import typing
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.types.network import NetworkReference
from stests.core.types.utils import get_isodatetime_field



@dataclass_json
@dataclass
class GeneratorArgs:
    """Arguments passed into generator from command line, rundeck ...etc.
    
    """
    # This is a placeholder class sub-classed by generators.
    pass


@dataclass_json
@dataclass
class GeneratorReference:
    """Encpasulates enough information to identify a generator run.
    
    """
    # Numerical index to distinguish between multiple runs of the same generator.
    index: int

    # Type of generator, e.g. WG-100 ...etc.
    typeof: str


    @property
    def cache_key(self):
        """Returns key to be used when caching an instance."""
        return f"{self.typeof}:R-{str(self.index).zfill(5)}"


    @classmethod
    def create(cls, index: int, typeof: str):
        """Factory method: leveraged in both live & test settings.

        """
        return GeneratorReference(index, typeof.upper())


@dataclass_json
@dataclass
class GeneratorContext:
    """Information collected eact time a generator is executed.
    
    """
    # Arguments passed into generator from command line, rundeck ...etc.
    args: GeneratorArgs

    # Associated network reference information.
    network: NetworkReference

    # Associated node reference information.
    node: int

    # Numerical index to distinguish between multiple runs of the same generator.
    run: int

    # Type of generator being executed.
    typeof: str

    # Standard time stamps.
    _ts_created: datetime = get_isodatetime_field(True)
    _ts_updated: datetime = get_isodatetime_field(True)


    @classmethod
    def create(
        cls,
        args: GeneratorArgs,
        network: str,
        node: int,
        run: int,
        typeof: str
        ):
        """Simple factory method.

        """
        return GeneratorContext(
            args=args,
            network=NetworkReference.create(network),
            node=node,
            typeof=typeof,
            run=run
        )
