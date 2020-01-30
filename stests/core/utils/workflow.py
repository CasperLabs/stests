import argparse
import typing
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.utils import env



@dataclass_json
@dataclass
class WorkflowContext():
    """Encpasulates information relevant to a workflow's execution context.
    
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
        cls = cls or WorkflowContext
        instance = cls(
            network_id=parsed.network_id,
            workflow_id=0,
            workflow_type = workflow_type
        )
        for i, j in parsed._get_kwargs():
            setattr(instance, i, j)

        return instance

