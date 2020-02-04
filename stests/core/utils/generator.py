import argparse
import typing
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.utils import env
from stests.core.utils import encoder
from stests.core.types import GeneratorReference
from stests.core.types import NetworkReference



@dataclass_json
@dataclass
class GeneratorScope:
    """Encapsulates generator scope information such as network identifier.
    
    """
    # Associated network reference information.
    network: NetworkReference

    # Index of node being tested.
    node_idx: int

    # Associated generator reference information.
    generator: GeneratorReference


    @property
    def generator_id(self):
        """Fully qualified generator identifier."""
        return f"{self.network.name}.{self.generator.typeof}.R-{str(self.generator.index).zfill(4)}"


    @property
    def network_id(self):
        """Fully qualified network identifier."""
        return f"{self.network_type.name}-{str(self.network_idx).zfill(2)}"


    @staticmethod
    def create(typeof: str, args: argparse.Namespace):
        """Simple factory method.

        :param args: Parsed command line arguments.
        :returns: Generator context information.

        """
        return GeneratorScope(
            generator=GeneratorReference.create(args.run_idx, typeof),
            network=NetworkReference.create(args.network),
            node_idx = 'node_idx' in args and args.node_idx
        )


# Ensure can be encoded/decoded off the wire.
encoder.register_type(GeneratorScope)


@dataclass_json
@dataclass
class GeneratorContext():
    """Encpasulates information relevant to a workflow's execution context.
    
    """
    # Scope within which generator is being executed.
    scope: GeneratorScope

    @property
    def generator_id(self):
        """Fully qualified generator identifier."""
        return self.scope.generator_id

    @property
    def network_id(self):
        """Fully qualified network identifier."""
        return self.scope.network_id


    @classmethod
    def execute(cls, args: argparse.Namespace):
        """Executes generator.
        
        :param args: Command line arguments.
        :param factory: Workflow factory.

        """
        # Register context class with encoder.
        encoder.register_type(cls)

        # Set context to be passed to actors.
        ctx = cls.create(args)
