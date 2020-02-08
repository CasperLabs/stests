from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.domain.enums import get_enum_field
from stests.core.domain.enums import DeployStatus
from stests.core.domain.meta import TypeMetadata



@dataclass_json
@dataclass
class Deploy:
    """Encapsulates information pertaining to a deploy dispatched to a test network.
    
    """
    # Deploy's payload signature hash (blake). 
    hash_id: str

    # Deploy's processing status.
    status: DeployStatus = get_enum_field(DeployStatus)

    # Associated metadata.
    meta: TypeMetadata
