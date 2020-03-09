import dataclasses
import typing
from datetime import datetime

from stests.core.orchestration.enums import ExecutionStatus
from stests.core.utils.dataclasses import get_timestamp_field



@dataclasses.dataclass
class ExecutionContextInfo:
    """Execution context information - run.
    
    """
    # Associated run arguments.
    args: typing.Optional[typing.Any]

    # Number of times to loop.
    loop_count: int

    # Upon successful completion of a run, the number of seconds after which a new run will be started.
    loop_interval: int

    # Associated network.
    network: str

    # Associated node index.
    node_index: int

    # Numerical index to distinguish between multiple runs.
    run_index: int

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

    # Timeperiod: run duration (in seconds).
    tp_duration: typing.Optional[float]

    # Timestamp: run start.
    ts_start: datetime

    # Timestamp: run end.
    ts_end: typing.Optional[datetime]

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    # Timestamp: create.
    _ts_created: datetime = get_timestamp_field()

    @property
    def tp_elapsed(self):
        if self.status == ExecutionStatus.COMPLETE:
            return self.tp_duration
        return datetime.now().timestamp() - self.ts_start.timestamp()

    @property
    def tp_duration_label(self):
        """Returns step duration formatted for display purposes.
        
        """
        if self.tp_duration is None:
            return "N/A"

        duration = str(self.tp_duration)
        minutes = duration.split(".")[0]
        seconds = duration.split(".")[1][:6]
        
        return f"{minutes}.{seconds}"

    @property
    def tp_elapsed_label(self):
        """Returns step elapsed formatted for display purposes.
        
        """
        elapsed = str(self.tp_elapsed)
        minutes = elapsed.split(".")[0]
        seconds = elapsed.split(".")[1][:6]
        
        return f"{minutes}.{seconds}"

    @property
    def run_index_label(self):
        return f"R-{str(self.run_index).zfill(3)}"

    @property
    def phase_index_label(self):
        return f"P-{str(self.phase_index).zfill(2)}"        

    @property
    def step_index_label(self):
        return f"S-{str(self.step_index).zfill(2)}"

    @property
    def next_phase_index(self):
        return self.phase_index + 1

    @property
    def next_phase_index_label(self):
        return f"P-{str(self.next_phase_index).zfill(2)}"        

    @property
    def next_step_index(self):
        return self.step_index + 1

    @property
    def next_step_index_label(self):
        return f"S-{str(self.next_step_index).zfill(2)}"


    def start(self):
        """Executed when run is about to start.
        
        """
        self.status = ExecutionStatus.IN_PROGRESS
        self.ts_start = datetime.now()

    
    def end(self, status, error=None):
        """Executed when run is complete.
        
        """
        self.error = error
        self.status = status
        self.ts_end = datetime.now()
        self.tp_duration = self.ts_end.timestamp() - self.ts_start.timestamp()

