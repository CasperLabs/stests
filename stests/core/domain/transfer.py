import dataclasses
import typing
from datetime import datetime

from stests.core.utils.dataclasses import get_timestamp_field
from stests.core.domain.enums import TransferStatus

    

@dataclasses.dataclass
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
    deploy_hash_refund: typing.Optional[str]

    # Flag indicating whether a refund is required.
    is_refundable: bool

    # Associated network.
    network: str

    # Associated node index.
    node: int

    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: int

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str    

    # Status of transfer.
    status: TransferStatus

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    # Timestamp: create.
    _ts_created: datetime = get_timestamp_field()


    def update_on_completion(self):
        """Executed when transfer has been completed.
        
        """
        self.status = TransferStatus.COMPLETE
