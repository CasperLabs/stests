from dataclasses import dataclass



@dataclass
class ExecutionRunLock:
    """Execution lock information - run.
    
    """
    # Associated network.
    network: str

    # Numerical index to distinguish between multiple runs of the same workflow.
    run_index: int

    # Type of workflow, e.g. WG-100 ...etc.
    run_type: str

    @property
    def run_index_label(self):
        return f"R-{str(self.run_index).zfill(3)}"


@dataclass
class ExecutionPhaseLock:
    """Execution lock information - phase.
    
    """
    # Associated network.
    network: str

    # Numerical index to distinguish between multiple runs of the same workflow.
    run_index: int

    # Type of workflow, e.g. WG-100 ...etc.
    run_type: str

    # Numerical index to distinguish between multiple phases within a run.
    phase_index: int

    @property
    def run_index_label(self):
        return f"R-{str(self.run_index).zfill(3)}"

    @property
    def phase_index_label(self):
        return f"P-{str(self.phase_index).zfill(2)}"


@dataclass
class ExecutionStepLock:
    """Execution lock information - step.
    
    """
    # Associated network.
    network: str

    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: int

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str

    # Numerical index to distinguish between multiple phases within a run.
    phase_index: int

    # Numerical index to distinguish between multiple steps within a phase.
    step_index: int

    @property
    def run_index_label(self):
        return f"R-{str(self.run_index).zfill(3)}"

    @property
    def phase_index_label(self):
        return f"P-{str(self.phase_index).zfill(2)}"

    @property
    def step_index_label(self):
        return f"S-{str(self.step_index).zfill(2)}"
