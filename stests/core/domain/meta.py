import datetime
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.utils.domain import get_isodatetime_field
from stests.core.utils.domain import get_uuid_field



@dataclass_json
@dataclass
class TypeMetadata:
    """Meta information associated with all domain types.
    
    """
    # Type key of associated object used in serialisation scenarios.
    type_key: str = None

    # Timestamp: create.
    ts_created: datetime = get_isodatetime_field(True)

    # Timestamp: update.
    ts_updated: datetime = get_isodatetime_field(True)

    # Universally unique identifier.
    uid: str = get_uuid_field(True) 



@dataclass_json
@dataclass
class DeployMetadata(TypeMetadata):
    """Meta information associated with all domain types.
    
    """
    pass
