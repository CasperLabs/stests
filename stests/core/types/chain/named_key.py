import dataclasses
import typing

from stests.core.types.chain.enums import ContractType



@dataclasses.dataclass
class NamedKey:
    """Account's can be associated with named keys, some of those keys are used in testing.
    
    """
    # On-chain account identifier.
    account_key: str

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

    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: typing.Optional[int]

    # Type of generator, e.g. WG-100 ...etc.
    run_type: typing.Optional[str]    

    @property
    def hash_as_bytes(self):
        return bytes.fromhex(self.hash)    

    @property
    def label_account_index(self):
        return f"A-{str(self.account_index).zfill(6)}"

    @property
    def label_run_index(self):
        return f"R-{str(self.run_index).zfill(3)}"

