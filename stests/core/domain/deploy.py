import typing
from dataclasses import dataclass
from datetime import datetime

from stests.core.domain.enums import DeployStatus
from stests.core.domain.enums import DeployType
from stests.core.utils.domain import *



@dataclass
class Deploy(Entity):
    """Encapsulates information pertaining to a deploy dispatched to a test network.
    
    """
    # Associated block hash in event of finalization. 
    block_hash: str

    # Deploy's payload signature hash (blake). 
    deploy_hash: str

    # Associated network.
    network: str

    # Associated node index.
    node: int

    # Numerical index to distinguish between multiple runs of the same generator.
    run: int

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str    

    # Deploy's processing status.
    status: DeployStatus

    # Time between dispatch & deploy finality.
    time_to_finalization: typing.Optional[float]

    # Flag indicating whether time to finalization was acceptable.
    time_to_finalization_is_acceptable: typing.Optional[bool]

    # Tolerance of time between dispatch & deploy finality.
    time_to_finalization_tolerance: typing.Optional[float]

    # Moment in time when deploy dispatched to CLX network.
    ts_dispatched: typing.Optional[datetime]

    # Moment in time when deploy was finalized by CLX network.
    ts_finalized: typing.Optional[datetime]

    # Deploy's processing status.
    typeof: DeployType

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    # Timestamp: create.
    _ts_created: datetime = get_timestamp_field()

    # Timestamp: update.
    _ts_updated: typing.Optional[datetime] = None

    # Universally unique identifier.
    _uid: str = get_uuid_field() 


    def update_on_finalization(self, bhash: str, ts_finalized: float):
        """Executed when deploy has been finalized.
        
        """
        self.block_hash = bhash
        self.status = DeployStatus.FINALIZED
        self.ts_finalized = datetime.fromtimestamp(ts_finalized)
        self.time_to_finalization = ts_finalized - self.ts_dispatched.timestamp()
