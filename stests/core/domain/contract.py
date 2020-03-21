import dataclasses
import typing
from datetime import datetime

from stests.core.domain.enums import AccountContractType
from stests.core.domain.enums import NetworkContractType
from stests.core.utils.dataclasses import get_timestamp_field



@dataclasses.dataclass
class AccountContract:
    """A contract associated with an account.
    
    """
    # Numerical index to distinguish between multiple accounts.
    account_index: int

    # Hash key that points to the stored contract.
    contract_hash: str

    # Associated network.
    network: typing.Optional[str]
    
    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: typing.Optional[int]

    # Type of generator, e.g. WG-100 ...etc.
    run_type: typing.Optional[str]

    # Type of client contract.
    typeof: AccountContractType

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    # Timestamp: create.
    _ts_created: datetime = get_timestamp_field()

    @property
    def label_account_index(self):
        return f"A-{str(self.account_index).zfill(6)}"

    @property
    def label_run_index(self):
        return f"R-{str(self.run_index).zfill(3)}"


@dataclasses.dataclass
class NetworkContract:
    """A test network.
    
    """
    # Hash key that points to the stored contract.
    chash: str

    # Associated network.
    network: typing.Optional[str]
    
    # Type of client contract.
    typeof: NetworkContractType

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    # Timestamp: create.
    _ts_created: datetime = get_timestamp_field()

