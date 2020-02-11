from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.domain.enums import DeployStatus
from stests.core.utils.domain import get_enum_field
from stests.core.utils.domain import TypeMetadata



@dataclass_json
@dataclass
class Deploy:
    """Encapsulates information pertaining to a deploy dispatched to a test network.
    
    """
    # Deploy's payload signature hash (blake). 
    hash_id: str

    # Deploy's processing status.
    status: DeployStatus = get_enum_field(DeployStatus)

    # Moment in time when  deploy dispatched to CLX network.
    ts_dispatched: int

    # Associated metadata.
    meta: TypeMetadata = TypeMetadata()