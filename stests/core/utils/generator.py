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
    run_idx: int

    # Type of generator being executed.
    typeof: str


    def __init__(self, typeof, args):
        """Constructor.

        :param args: Parsed command line arguments.
        
        """
        self.network_idx = args.network_idx
        self.network_type = args.network_type
        self.run_idx = args.generator_run_idx
        self.typeof = generator_type

    @property
    def cache_namespace(self):
        """Derived cache namespace."""
        return f"{self.generator_type}.{self.generator_run_idx}"


@dataclass_json
@dataclass
class GeneratorArguments:
    """Encapsulates generator arguments passed in from command line.
    
    """
    def __init__(self, args):
        """Constructor.

        :param args: Parsed command line arguments.
        
        """
        excluded = [
            'network_idx',
            'network_type',
            'generator_run_idx'
        ]
        for i, j in [(i, j) for i, j in args._get_kwargs() if i not in excluded]:
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
    def create(
        typeof: str,
        args_cls: GeneratorArguments,
        cli_args: argparse.Namespace
        ):
        """Simple factory method t o instantiate form command line arguments.
        
        """
        return GeneratorContext(
            GeneratorArgs(args),
            GeneratorScope(typeof, args)
        )
