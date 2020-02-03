import enum
from dataclasses import dataclass
from datetime import datetime

from stests.core.types.enums import get_enum_field
from stests.core.types.enums import DeployStatus
from stests.core.types.network import NetworkEntity
from stests.core.types.utils import get_isodatetime_field



@dataclass_json
@dataclass
class Deploy(NetworkEntity):
    """Encapsulates information pertaining to a deploy dispatched to a test network.
    
    """
    # Deploy's payload signature hash (blake). 
    hash_id: str

    # Deploy's processing status.
    status: DeployStatus = get_enum_field(DeployStatus)

    # Standard time stamps.
    _ts_updated: datetime = get_isodatetime_field(True)
    _ts_created: datetime = get_isodatetime_field(True)


    @staticmethod
    def create():
        """Factory: returns an instance for testing purposes.
        
        """
        return Deploy(
            hash_id="6ff843ba685842aa82031d3f53c48b66326df7639a63d128974c5c14f31a0f33343a8c65551134ed1ae0f2b0dd2bb495dc81039e3eeb0aa1bb0388bbeac29183",
            status=DeployStatus.NULL
        )
