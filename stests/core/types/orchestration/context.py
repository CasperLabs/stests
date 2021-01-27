import dataclasses
import typing

from stests.core.types.orchestration.enums import ExecutionStatus
from stests.core.types.orchestration.enums import ExecutionMode



@dataclasses.dataclass
class ExecutionContext:
    """Execution context information - i.e. a run.
    
    """
    # Associated run arguments.
    args: typing.Optional[typing.Any]

    # Flag indicating whether post run pruning is automated.
    prune_on_completion: bool

    # Number of deploys to dispatch per second.
    deploys_per_second: int

    # Mode of execution.
    execution_mode: ExecutionMode

    # Algorithm to use when generating keys during the course of a run.
    key_algorithm: str

    # Number of times to loop.
    loop_count: int

    # Numerical index to distinguish between loops.
    loop_index: int

    # The number of milli-seconds after which a new run will be started.
    loop_interval_ms: int

    # Associated network.
    network: str

    # Associated node index.
    node_index: int

    # Numerical index to distinguish between multiple runs.
    run_index: int

    # Index of parent run in a loop scenario.
    run_index_parent: typing.Optional[int]

    # Type of run, e.g. WG-100 ...etc.
    run_type: str

    # Index to disambiguate a phase within the context of a run.
    phase_index: int

    # Current status.
    status: ExecutionStatus

    # Index to disambiguate a step within the context of a phase.
    step_index: int

    # Label to disambiguate a step within the context of a phase.
    step_label: typing.Optional[str]

    # Unique identifier to disambiguate runs.
    uid: str

    @property
    def next_phase_index(self):
        return self.phase_index + 1

    @property
    def label_next_phase_index(self):
        return f"P-{str(self.next_phase_index).zfill(2)}"        

    @property
    def next_step_index(self):
        return self.step_index + 1

    @property
    def label_next_step_index(self):
        return f"S-{str(self.next_step_index).zfill(2)}"

    @property
    def label_step(self):
        return f"{self.label_phase_index}.{self.label_step_index}"

    @property
    def label_run_index(self):
        return f"R-{str(self.run_index).zfill(3)}"

    @property
    def label_phase_index(self):
        return f"P-{str(self.phase_index).zfill(2)}"        

    @property
    def label_step_index(self):
        return f"S-{str(self.step_index).zfill(2)}"


    def get_dispatch_window_ms(self, deploy_count):
        """Returns a time window during which deploys will be dispatched.
        
        """
        if self.deploys_per_second:
            return int((deploy_count / self.deploys_per_second) * 1000)
        return 0