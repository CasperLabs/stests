import dataclasses
import typing

from stests.core.types.chain.enums import ContractType



@dataclasses.dataclass
class NamedKey:
    """Account's can be associated with named keys, some of those keys are used in testing.
    
    """
    # Numerical index to distinguish between multiple accounts.
    account_index: int

    # Type of contract with which key is associated.
    contract_type: typing.Optional[ContractType]

    # Key hash.
    hash: typing.Optional[str]

    # Key name.
    name: typing.Optional[str]

    # Associated network.
    network: str

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    @property
    def hash_as_bytes(self):
        return bytes.fromhex(self.hash)    

    @property
    def label_account_index(self):
        return f"A-{str(self.account_index).zfill(6)}"
