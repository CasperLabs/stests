import dataclasses
import typing

from stests.core.types.chain.enums import TransferStatus

    

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

    # Numerical index to distinguish between multiple phase within a generator.
    phase_index: typing.Optional[int]

    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: int

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str    

    # Status of transfer.
    status: TransferStatus

    # Numerical index to distinguish between multiple steps within a generator.
    step_index: typing.Optional[int]

    # Label to disambiguate a step within the context of a phase.
    step_label: typing.Optional[str]

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

