from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.domain.enums import BlockStatus
from stests.core.domain.meta import TypeMetadata
from stests.core.utils.domain import get_enum_field

    

@dataclass_json
@dataclass
class Block:
    """A block proposed/finialized within the lifetime of a chain.
    
    """
    # Block hash (blake2b) identifier.
    bhash: str

    # Motes spent during block processing.
    deploy_cost_total: str

    # Number of deploys within block.
    deploy_count: str

    # Average price of deploys.
    deploy_gas_price_avg: int

    # Rank, aka height.
    rank: int

    # Size in bytes of block.
    size_bytes: int

    # Block consensus status, e.g. ADDED | FINALIZED ... etc.
    status: BlockStatus = get_enum_field(BlockStatus)

    # Block processing timestamp.
    timestamp: int

    # Validator identifier that proposed block.
    validator_id: str

    # Associated metadata.
    meta: TypeMetadata
