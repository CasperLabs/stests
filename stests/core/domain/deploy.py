import dataclasses
import typing
from datetime import datetime

from stests.core.domain.enums import DeployStatus
from stests.core.domain.enums import DeployType
from stests.core.utils.dataclasses import get_timestamp_field



@dataclasses.dataclass
class Deploy:
    """Encapsulates information pertaining to a deploy dispatched to a test network.
    
    """
    # Index of account with which the deploy is associated.
    account_index: typing.Optional[int]

    # Associated block hash in event of finalization. 
    block_hash: str

    # Deploy's payload signature hash (blake). 
    deploy_hash: str

    # Node to which deploy was dispatched.
    dispatch_node: int

    # Moment in time when deploy dispatched to CLX network.
    dispatch_ts: typing.Optional[datetime]

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

    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: int

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str    

    # Deploy's processing status.
    status: DeployStatus

    # Deploy's processing status.
    typeof: DeployType

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    # Timestamp: create.
    _ts_created: datetime = get_timestamp_field()


    @property
    def label_finalization_time(self):
        if self.finalization_time:
            return format(self.finalization_time, '.4f')
        return "--"


    def update_on_finalization(self, bhash: str, finalization_ts: float):
        """Executed when deploy has been finalized.
        
        """
        self.block_hash = bhash
        self.status = DeployStatus.FINALIZED
        self.finalization_ts = datetime.fromtimestamp(finalization_ts)
        self.finalization_time = finalization_ts - self.dispatch_ts.timestamp()
