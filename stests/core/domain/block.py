from dataclasses import dataclass

from stests.core.domain.enums import BlockStatus
from stests.core.utils.domain import *

    

@dataclass
class Block(Entity):
    """A block proposed/finialized within the lifetime of a chain.
    
    """
    # Block hash (blake2b) identifier.
    block_hash: str

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

    # Type key of associated object used in serialisation scenarios.
    _type_key: str = None

    # Timestamp: create.
    _ts_created: datetime = get_isodatetime_field(True)

    # Timestamp: update.
    _ts_updated: datetime = get_isodatetime_field(True)

    # Universally unique identifier.
    _uid: str = get_uuid_field(True) 
