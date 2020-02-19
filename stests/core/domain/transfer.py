from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.domain.meta import TypeMetadata

    

@dataclass_json
@dataclass
class Transfer:
    """Encapsulates information pertaining to a CLX transfer between counterparties.
    
    """
    # Amount in motes that was transferred.
    amount: int

    # Asset being transferred.
    asset: str

    # Counter-party 1 account index.
    cp1_index: int

    # Counter-party 2 account index.
    cp2_index: int

    # Associated deploy hash.
    deploy_hash: str

    # Associated deploy hash.
    deploy_hash_refund: str

    # Flag indicating whether a refund is required.
    is_refundable: bool

    # Associated metadata.
    meta: TypeMetadata = TypeMetadata()