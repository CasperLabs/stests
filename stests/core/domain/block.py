import dataclasses
import typing
from datetime import datetime

from stests.core.domain.enums import BlockStatus
from stests.core.utils.dataclasses import get_timestamp_field

    

@dataclasses.dataclass
class Block:
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

    # J-rank.
    j_rank: int

    # Main rank.
    m_rank: int

    # Associated network.
    network: str

    # Size in bytes of block.
    size_bytes: int

    # Block consensus status, e.g. ADDED | FINALIZED ... etc.
    status: BlockStatus

    # Block processing timestamp.
    timestamp: datetime

    # Validator identifier that proposed block.
    validator_id: str

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    # Timestamp: create.
    _ts_created: datetime = get_timestamp_field()

    @property
    def hash(self):
        return self.block_hash

    @property
    def label_m_rank(self):
        return f"{str(self.m_rank).zfill(7)}"

    def update_on_finalization(self):
        """Executed when block has been finalized.
        
        """
        self.status = BlockStatus.FINALIZED


@dataclasses.dataclass
class BlockLock:
    """Execution lock information - block.
    
    """
    # Block hash (blake2b) identifier.
    block_hash: str

    # Type of event for which the lock is being acquired.
    event_type: str

    # Associated network.
    network: str

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None
