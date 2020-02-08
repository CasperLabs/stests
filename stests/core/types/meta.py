from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime

from stests.core.types.utils import get_isodatetime_field
from stests.core.types.utils import get_uuid_field
from stests.core.utils import defaults




@dataclass_json
@dataclass
class TypeMetadata:
    """Meta information associated with all domain types.
    
    """
    # Identifier of network with which type instance is associated.
    network: str

    # Identifier of node with which type instance is associated.
    node: int

    # Identifier of run which instantiated type instance.
    run: int

    # Type of run which instantiated type instance.
    run_type: str    

    # Timestamp: create.
    ts_created: datetime = get_isodatetime_field(True)

    # Timestamp: update.
    ts_updated: datetime = get_isodatetime_field(True)

    # Universally unique identifier.
    uid: str = get_uuid_field(True) 
