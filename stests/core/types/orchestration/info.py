import dataclasses
import typing
from datetime import datetime

from stests.core.types.orchestration.enums import ExecutionAspect
from stests.core.types.orchestration.enums import ExecutionStatus



@dataclasses.dataclass
class ExecutionInfo:
    """Execution information.
    
    """
    # Aspect of execution to which this information pertains.
    aspect: ExecutionAspect

    # Associated network.
    network: str

    # Index to disambiguate a phase within the context of a run.
    phase_index: int

    # Numerical index to distinguish between multiple runs.
    run_index: int

    # Index of parent run in a loop scenario.
    run_index_parent: typing.Optional[int]

    # Type of run, e.g. WG-100 ...etc.
    run_type: str

    # Current status.
    status: ExecutionStatus

    # Index to disambiguate a step within the context of a phase.
    step_index: int

    # Label to disambiguate a step within the context of a phase.
    step_label: str

    # Timeperiod: run duration (in seconds).
    tp_duration: typing.Optional[float]

    # Timestamp: run start.
    ts_start: datetime

    # Timestamp: run end.
    ts_end: typing.Optional[datetime]


    @property
    def label_step_index(self):
        if self.step_index:
            return f"S-{str(self.step_index).zfill(2)}"
        return "    "

    @property
    def tp_elapsed(self):
        if self.status in (ExecutionStatus.COMPLETE, ExecutionStatus.ERROR):
            return self.tp_duration
        return datetime.utcnow().timestamp() - self.ts_start.timestamp()

    @property
    def label_tp_duration(self):
        """Returns step duration formatted for display purposes.
        
        """
        if self.tp_duration is None:
            return "N/A"

        duration = str(self.tp_duration)
        minutes = duration.split(".")[0]
        seconds = duration.split(".")[1][:6]
        
        return f"{minutes}.{seconds}"

    @property
    def label_tp_elapsed(self):
        """Returns step elapsed formatted for display purposes.
        
        """
        elapsed = str(self.tp_elapsed)
        minutes = elapsed.split(".")[0]
        seconds = elapsed.split(".")[1][:6]
        
        return f"{minutes}.{seconds}"

    @property
    def label_phase_index(self):
        if self.phase_index:
            return f"P-{str(self.phase_index).zfill(2)}"
        return "    "

    @property
    def label_run_index(self):
        return f"R-{str(self.run_index).zfill(3)}"

    @property
    def label_status(self):
        return self.status.name.ljust(10)

    @property
    def label_index(self):
        if self.aspect == ExecutionAspect.RUN:
            return self.label_run_index.ljust(15)
        elif self.aspect == ExecutionAspect.PHASE:
            return f"{self.label_run_index}.{self.label_phase_index.ljust(9)}"
        elif self.aspect == ExecutionAspect.STEP:
            return f"{self.label_run_index}.{self.label_phase_index}.{self.label_step_index}"



    def end(self, status, error=None):
        """Invoked when execution is complete.
        
        """
        self.error = error
        self.status = status
        self.ts_end = datetime.utcnow()
        self.tp_duration = self.ts_end.timestamp() - self.ts_start.timestamp()
