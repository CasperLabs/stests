from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.domain.enums import DeployStatus
from stests.core.domain.meta import TypeMetadata
from stests.core.utils.domain import get_enum_field



@dataclass_json
@dataclass
class Deploy:
    """Encapsulates information pertaining to a deploy dispatched to a test network.
    
    """
    # Associated block hash in event of finalization. 
    block_hash: str

    # Associated block rank in event of finalization. 
    block_rank: int

    # Deploy's payload signature hash (blake). 
    deploy_hash: str

    # Deploy's processing status.
    status: DeployStatus = get_enum_field(DeployStatus)

    # Moment in time when deploy dispatched to CLX network.
    ts_dispatched: int

    # Moment in time when deploy was finalized by CLX network.
    ts_finalized: int

    # Associated network.
    network: str

    # Associated node index.
    node: int

    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: int

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str    

    # Associated metadata.
    meta: TypeMetadata = TypeMetadata()