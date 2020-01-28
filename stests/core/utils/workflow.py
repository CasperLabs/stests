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

    @property
    def cache_namespace(self):
        return f"{self.workflow_type}.{self.workflow_id}"


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


@dataclass_json
@dataclass
class WorkflowContext():
    """Encpasulates information & services relevant to current execution context.
    
    """
    # Execution arguments pass along execution thread.
    args: WorkflowArguments

    @property
    def network_id(self):
        return self.args.network_id

    @property
    def workflow_id(self):
        return self.args.workflow_id

    @property
    def workflow_type(self):
        return self.args.workflow_type

    @property
    def cache_namespace(self):
        return f"{self.workflow_type}.{self.workflow_id}"


    @staticmethod
    def create(args: WorkflowArguments):
        """Returns an instance ready for use within a workflow.

        :param args: Workflow arguments typically derived from command line.
        :returns: A context instance configured for use by actors.

        """        
        return WorkflowContext(args)
