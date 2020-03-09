import dataclasses

from stests.core.orchestration.enums import ExecutionStatus



@dataclasses.dataclass
class ExecutionRunState:
    """Run execution state information.
    
    """
    # Associated network.
    network: str

    # Numerical index to distinguish between multiple runs.
    run_index: int

    # Type of run, e.g. WG-100 ...etc.
    run_type: str

    # Execution status.
    status: ExecutionStatus

    # Type key of associated object used in serialisation scenarios.
    _type_key: str

    @property
    def run_index_label(self):
        return f"R-{str(self.run_index).zfill(3)}"
        

@dataclasses.dataclass
class ExecutionPhaseState(ExecutionRunState):
    """Phase execution state information.
    
    """
    # Index within the context of a pipeline.
    phase_index: int

    @property
    def phase_index_label(self):
        return f"P-{str(self.phase_index).zfill(2)}"


@dataclasses.dataclass
class ExecutionStepState(ExecutionPhaseState):
    """Step execution state information.
    
    """
    # Index to disambiguate a step within the context of a phase.
    step_index: int

    # Label to disambiguate a step within the context of a phase.
    step_label: str

    @property
    def step_index_label(self):
        return f"S-{str(self.step_index).zfill(2)}"
