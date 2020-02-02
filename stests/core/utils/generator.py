import argparse
import typing
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.utils import env
from stests.core.utils import encoder
from stests.core.types import NetworkType



@dataclass_json
@dataclass
class GeneratorScope:
    """Encapsulates generator scope informatino such as network identifier.
    
    """
    # Index of network being tested.
    network_idx: int

    # Type of network being tested.
    network_type: NetworkType

    # Index of node being tested.
    node_idx: int

    # Run index of generator being executed.
    run_idx: int

    # Type of generator being executed.
    typeof: str

    @property
    def cache_namespace(self):
        """Derived cache namespace."""
        return f"{self.typeof}.{self.run_idx}"

    @property
    def network_id(self):
        """Derived network id."""
        return f"{self.network_type}-{str(self.network_idx).zfill(2)}"


    @staticmethod
    def create(typeof: str, args: argparse.Namespace):
        """Simple factory method.

        :param args: Parsed command line arguments.
        :returns: Generator context information.

        """
        return GeneratorScope(
            network_idx = 'network_idx' in args and args.network_idx,
            network_type = 'network_type' in args and NetworkType[args.network_type.upper()].name,
            node_idx = 'node_idx' in args and args.node_idx,
            run_idx = 'run_idx' in args and args.run_idx,
            typeof = typeof.upper() 
        )



@dataclass_json
@dataclass
class GeneratorContext():
    """Encpasulates information relevant to a workflow's execution context.
    
    """
    # Scope within which generator is being executed.
    scope: GeneratorScope


    @classmethod
    def execute(cls, args: argparse.Namespace, factory: typing.Callable):
        """Executes generator.
        
        :param args: Command line arguments.
        :param factory: Workflow factory.

        """
        # Register context class with encoder.
        encoder.register_type(cls)

        # Set context to be passed to actors.
        ctx = cls.create(args)

        # Initialise broker.
        from stests.core import mq
        mq.init_broker()

        # Instantiate workflow.
        workflow = factory(ctx)
        workflow.run()
