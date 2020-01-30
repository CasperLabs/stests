import argparse
import typing
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.utils import env
from stests.core.types import NetworkType



@dataclass_json
@dataclass
class GeneratorScope:
    """Encapsulates generator scope informatino such as network identifier.
    
    """
    # Type of network being tested.
    network_type: NetworkType

    # Index of network being tested.
    network_idx: int

    # Run index of generator being executed.
    generator_run_idx: int

    # Type of generator being executed.
    generator_type: str


    def __init__(self, generator_type, args):
        """Constructor.

        :param args: Parsed command line arguments.
        
        """
        self.network_idx = args.network_idx
        self.network_type = args.network_type
        self.generator_run_idx = args.generator_run_idx
        self.generator_type = generator_type

    @property
    def cache_namespace(self):
        """Derived cache namespace."""
        return f"{self.generator_type}.{self.generator_run_idx}"


@dataclass_json
@dataclass
class GeneratorArgs:
    """Encapsulates generator arguments passed in from command line.
    
    """
    def __init__(self, args):
        """Constructor.

        :param args: Parsed command line arguments.
        
        """
        # Injected comand line arguments.
        for i, j in args._get_kwargs():
            setattr(self, i, j)


@dataclass_json
@dataclass
class GeneratorContext():
    """Encpasulates information relevant to a workflow's execution context.
    
    """
    # Scope within which generator is being executed.
    args: GeneratorArgs

    # Scope within which generator is being executed.
    scope: GeneratorScope

    @property
    def cache_namespace(self):
        return self.scope.cache_namespace


    @staticmethod
    def create(generator_type: str, args: argparse.Namespace):
        """Simple factory method t o instantiate form command line arguments.
        
        """
        return GeneratorContext(
            GeneratorArgs(args),
            GeneratorScope(generator_type, args)
        )
