import dataclasses
import typing

from stests.core.domain.enums import AccountStatus
from stests.core.domain.enums import AccountType
from stests.core.domain.key_pair import PrivateKey
from stests.core.domain.network import NetworkIdentifier


@dataclasses.dataclass
class Account:
    """A non-designated account that maps to an address upon target chain.
    
    """
    # Numerical index to distinguish between multiple accounts within same run.
    index: int

    # Associated network.
    network: typing.Optional[str]

    # Associated node index.
    node: typing.Optional[int]

    # Hexadecimal representation of private key used primarily in signing scenarios.
    private_key: str

    # Hexadecimal representation of public key used primarily in identity & verification scenarios.
    public_key: str

    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: typing.Optional[int]

    # Type of generator, e.g. WG-100 ...etc.
    run_type: typing.Optional[str]

    # Current account status.
    status: AccountStatus

    # Type of account, e.g. USER | FAUCET | BOND | CONTRACT.
    typeof: AccountType

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    @property
    def private_key_as_pem_filepath(self):
        return PrivateKey(self.private_key).as_pem_filepath

    @property
    def label_index(self):
        return f"A-{str(self.index).zfill(6)}"


@dataclasses.dataclass
class AccountIdentifier:
    """Information required to disambiguate between accounts.
    
    """ 
    # Numerical index to distinguish between accounts within same context.
    index: int

    # Associated run identifier.
    run: typing.Any

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    @property
    def network_id(self) -> NetworkIdentifier:
        return this.run.network

    @property
    def label_index(self):
        return f"A-{str(self.index).zfill(6)}"


