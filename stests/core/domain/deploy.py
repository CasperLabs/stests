import dataclasses
import typing
from datetime import datetime

from stests.core.domain.block import Block
from stests.core.domain.enums import DeployStatus
from stests.core.domain.enums import DeployType



@dataclasses.dataclass
class Deploy:
    """Encapsulates information pertaining to a deploy dispatched to a test network.
    
    """
    # Index of account with which the deploy is associated.
    account_index: typing.Optional[int]

    # Associated block hash in event of finalization. 
    block_hash: typing.Optional[str]

    # Cost of deploy (in motes).
    cost: typing.Optional[int]

    # Deploy's payload signature hash (blake). 
    deploy_hash: str

    # Node to which deploy was dispatched.
    dispatch_node: int

    # Moment in time when deploy dispatched to CLX network.
    dispatch_ts: typing.Optional[datetime]

    # Node which emitted finalization event of the block in which deploy was included.
    finalization_node: typing.Optional[int]

    # Time between dispatch & deploy finality.
    finalization_time: typing.Optional[float]

    # Flag indicating whether time to finalization was acceptable.
    finalization_time_is_acceptable: typing.Optional[bool]

    # Tolerance of time between dispatch & deploy finality.
    finalization_time_tolerance: typing.Optional[float]
    
    # Moment in time when deploy was finalized by CLX network.
    finalization_ts: typing.Optional[datetime]

    # Associated network.
    network: str

    # Numerical index to distinguish between multiple phase within a generator.
    phase_index: typing.Optional[int]

    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: int

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str    

    # Numerical index to distinguish between multiple steps within a generator.
    step_index: typing.Optional[int]

    # Label to disambiguate a step within the context of a phase.
    step_label: typing.Optional[str]

    # Deploy's processing status.
    status: DeployStatus

    # Deploy's processing status.
    typeof: DeployType

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    @property
    def hash(self):
        return self.deploy_hash

    @property
    def is_from_run(self):
        return self.run_type is not None
        
    @property
    def label_finalization_time(self):
        if self.finalization_time:
            return format(self.finalization_time, '.4f')
        return "--"

    @property
    def label_account_index(self):
        return f"A-{str(self.account_index).zfill(6)}"

    @property
    def label_phase_index(self):
        return f"P-{str(self.phase_index).zfill(2)}"

    @property
    def label_run_index(self):
        return f"R-{str(self.run_index).zfill(3)}"

    @property
    def label_step_index(self):
        return f"S-{str(self.step_index).zfill(2)}"
