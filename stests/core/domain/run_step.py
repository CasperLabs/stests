import typing
from dataclasses import dataclass
from datetime import datetime

from stests.core.domain.enums import ExecutionStatus
from stests.core.utils.domain import *



@dataclass
class RunStep(Entity):
    """Step information associated with a generator run.
    
    """
    # Associated network.
    network: str

    # Index within the context of a pipeline.
    pipeline_index: str

    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: int

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str

    # Current status.
    status: ExecutionStatus

    # Index to disambiguate a step within the context of a phase.
    step_index: int

    # Elapsed execution time (in seconds).
    step_duration: typing.Optional[float]

    # Moment in time when step occurred.
    ts_start: datetime

    # Moment in time when step completed.
    ts_end: typing.Optional[datetime]

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    # Timestamp: create.
    _ts_created: datetime = get_timestamp_field()

    @property
    def ts_elapsed(self):
        if self.status == ExecutionStatus.COMPLETE:
            return self.step_duration
        return datetime.now().timestamp() - self.ts_start.timestamp()

    @property
    def step_duration_label(self):
        """Returns step duration formatted for display purposes.
        
        """
        if self.step_duration is None:
            return "N/A"

        duration = str(self.step_duration)
        minutes = duration.split(".")[0]
        seconds = duration.split(".")[1][:6]
        
        return f"{minutes}.{seconds}"

    @property
    def step_elapsed_label(self):
        """Returns step elapsed formatted for display purposes.
        
        """
        elapsed = str(self.ts_elapsed)
        minutes = elapsed.split(".")[0]
        seconds = elapsed.split(".")[1][:6]
        
        return f"{minutes}.{seconds}"

    @property
    def phase_index_label(self):
        return f"P-{str(self.phase_index).zfill(2)}"

    @property
    def run_index_label(self):
        return f"R-{str(self.run_index).zfill(3)}"

    @property
    def step_index_label(self):
        return f"S-{str(self.step_index).zfill(2)}"


    def update_on_completion(self):
        """Executed when transfer has been completed.
        
        """
        self.status = ExecutionStatus.COMPLETE
        self.ts_end = datetime.now()
        self.step_duration = self.ts_end.timestamp() - self.ts_start.timestamp()



@dataclass
class ExecutionStepState(Entity):
    """Execution state information - step.
    
    """
    # Associated network.
    network: str

    # Index to disambiguate a phase within the context of a run.
    phase_index: int

    # Index to distinguish between multiple runs.
    run_index: int

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str

    # Index to disambiguate a step within the context of a phase.
    step_index: int

    # Label to disambiguate a step within the context of a phase.
    step_label: str

    # Current status.
    status: ExecutionStatus

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    # Timestamp: create.
    _ts_created: datetime = get_timestamp_field()

    @property
    def phase_index_label(self):
        return f"P-{str(self.phase_index).zfill(2)}"

    @property
    def run_index_label(self):
        return f"R-{str(self.run_index).zfill(3)}"

    @property
    def step_index_label(self):
        return f"S-{str(self.step_index).zfill(2)}"
