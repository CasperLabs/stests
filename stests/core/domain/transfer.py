import typing
from dataclasses import dataclass

from stests.core.utils.domain import *
from stests.core.domain.enums import TransferStatus

    

@dataclass
class Transfer(Entity):
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
    deploy_hash_refund: typing.Union[None, str]

    # Flag indicating whether a refund is required.
    is_refundable: bool

    # Associated network.
    network: str

    # Associated node index.
    node: int

    # Numerical index to distinguish between multiple runs of the same generator.
    run: int

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str    

    # Status of transfer.
    status: TransferStatus = get_enum_field(TransferStatus)

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Union[None, str] = None

    # Timestamp: create.
    _ts_created: datetime = get_isodatetime_field(True)

    # Timestamp: update.
    _ts_updated: datetime = get_isodatetime_field(True)

    # Universally unique identifier.
    _uid: str = get_uuid_field(True) 
