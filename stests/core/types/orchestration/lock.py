import dataclasses
import typing

from stests.core.types.orchestration.enums import ExecutionAspect



@dataclasses.dataclass
class ExecutionLock:
    """Execution lock information.
    
    """
    # Aspect of execution to which a lock applies.
    aspect: ExecutionAspect

    # Associated network.
    network: str

    # Numerical index to distinguish between multiple phases within a run.
    phase_index: typing.Optional[int]

    # Numerical index to distinguish between multiple runs of the same workflow.
    run_index: int

    # Type of workflow, e.g. WG-100 ...etc.
    run_type: str

    # Numerical index to distinguish between multiple steps within a phase.
    step_index: int

    @property
    def label_phase_index(self):
        if self.phase_index:
            return f"P-{str(self.phase_index).zfill(2)}"

    @property
    def label_run_index(self):
        return f"R-{str(self.run_index).zfill(3)}"

    @property
    def label_step_index(self):
        if self.step_index:
            return f"S-{str(self.step_index).zfill(2)}"
