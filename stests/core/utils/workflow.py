import argparse
import typing
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.utils import env



@dataclass_json
@dataclass
class WorkflowArguments():
    """Arguments associated with workflow execution.
    
    """
    # Identifier of network being tested.
    network_id: str

    # Identifier of workflow instance being executed.
    workflow_id: int

    # Type of workflow being executed.
    workflow_type: str


    @staticmethod
    def create(cls, workflow_type: str, parsed: argparse.Namespace):
        """Simple factory method.
        
        """
        cls = cls or WorkflowArguments
        instance = cls(
            network_id=parsed.network_id,
            workflow_id=0,
            workflow_type = workflow_type
        )
        for i, j in parsed._get_kwargs():
            setattr(instance, i, j)

        return instance


    @staticmethod
    def get_parser(description: str) -> argparse.ArgumentParser:
        """Returns default workflow command line argument parser.

        : param description: Short text describing intent of workflow.
        : returns: Default workflow CLI argument parser.

        """
        # Set command line arguments.
        parser = argparse.ArgumentParser(
            f"Executes the {description} workload generator."
        )

        # Network identifer.
        parser.add_argument(
            "--network-id",
            help="Identifier of network being tested.",
            dest="network_id",
            type=str,
            default=env.get_network_id()
            )

        # Workflow identifer.
        # TODO: derive from cache
        parser.add_argument(
            "--workflow-id",
            help="Identifier of workflow being executed.",
            dest="workflow_id",
            type=int,
            default=0
            )

        return parser


    @staticmethod
    def get_parser_for_workflow(description: str) -> argparse.ArgumentParser:
        """Returns default workflow command line argument parser.

        : param description: Short text describing intent of workflow.
        : returns: Default workflow CLI argument parser.

        """
        # Set command line arguments.
        parser = argparse.ArgumentParser(
            f"Executes the {description} worker."
        )

        # Network identifer.
        parser.add_argument(
            "--network-id",
            help="Identifier of network being tested.",
            dest="network_id",
            type=str,
            default=env.get_network_id()
            )

        return parser


class WorkflowServices():
    """Exposes services available to actors.
    
    """
    # Cache store accessor.
    cache: typing.Any


@dataclass_json
@dataclass
class WorkflowContext():
    """Encpasulates information & services relevant to current execution context.
    
    """
    # Execution arguments pass along execution thread.
    args: WorkflowArguments

    # Services unavailable to actors.
    # Note: not serialised.
    services: typing.ClassVar[WorkflowServices] 

    @property
    def network_id(self):
        return self.args.network_id

    @property
    def workflow_id(self):
        return self.args.workflow_id

    @property
    def workflow_type(self):
        return self.args.workflow_type


    @staticmethod
    def create(args: WorkflowArguments):
        """Returns an instance ready for use within a workflow.

        :param args: Workflow arguments typically derived from command line.
        :returns: A context instance configured for use by actors.

        """        
        ctx = WorkflowContext(args)
        ctx.set_services()

        return ctx


    def set_services(self):
        """Injects workflow servcies.
        
        """
        # JIT import to avoid circular references.
        from stests.core import cache

        self.services = WorkflowServices()
        self.services.cache = cache.get_store(self.args.network_id) 
