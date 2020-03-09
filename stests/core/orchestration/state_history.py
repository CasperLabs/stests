import dataclasses

from stests.core.orchestration.enums import ExecutionAspect
from stests.core.orchestration.enums import ExecutionStatus



@dataclasses.dataclass
class ExecutionState:
    """Execution state information.
    
    """
    # Aspect of execution to which this state information pertains.
    aspect: ExecutionAspect

    # Associated network.
    network: str

    # Index within the context of a pipeline.
    phase_index: int

    # Numerical index to distinguish between multiple runs.
    run_index: int

    # Type of run, e.g. WG-100 ...etc.
    run_type: str

    # Execution status.
    status: ExecutionStatus

    # Index to disambiguate a step within the context of a phase.
    step_index: int

    # Label to disambiguate a step within the context of a phase.
    step_label: str

    # Type key of associated object used in serialisation scenarios.
    _type_key: str

    @property
    def phase_index_label(self):
        return f"P-{str(self.phase_index).zfill(2)}"    

    @property
    def run_index_label(self):
        return f"R-{str(self.run_index).zfill(3)}"

    @property
    def step_index_label(self):
        return f"S-{str(self.step_index).zfill(2)}"


