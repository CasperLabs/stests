import dataclasses
import typing

from stests.core.types.chain.enums import AccountType
from stests.core.types.chain.key_pair import PrivateKey
from stests.core.types.chain.key_pair import PublicKey



@dataclasses.dataclass
class Account:
    """A non-designated account that maps to an address upon target chain.
    
    """
    # Numerical index to distinguish between multiple accounts within same run.
    index: int

    # Associated network.
    network: typing.Optional[str]

    # Hexadecimal representation of private key used primarily in signing scenarios.
    private_key: str

    # Hexadecimal representation of public key used primarily in identity & verification scenarios.
    public_key: str

    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: typing.Optional[int]

    # Type of generator, e.g. WG-100 ...etc.
    run_type: typing.Optional[str]

    # Type of account, e.g. USER | FAUCET | BOND | CONTRACT.
    typeof: AccountType

    @property
    def address(self):
        return self.public_key

    @property
    def is_run_account(self):
        return self.run_index is not None

    @property
    def private_key_as_bytes(self):
        return bytes.fromhex(self.private_key)

    @property
    def private_key_as_pem_filepath(self):
        return PrivateKey(self.private_key).as_pem_filepath

    @property
    def public_key_as_bytes(self):
        return bytes.fromhex(self.public_key)

    @property
    def public_key_as_pem_filepath(self):
        return PublicKey(self.public_key).as_pem_filepath

    @property
    def label_index(self):
        return f"A-{str(self.index).zfill(6)}"

    @property
    def label_run_index(self):
        return f"R-{str(self.run_index).zfill(3)}"


@dataclasses.dataclass
class AccountIdentifier:
    """Information required to disambiguate between accounts.
    
    """ 
    # Numerical index to distinguish between accounts within same context.
    index: int

    # Associated run identifier.
    run: typing.Any

    @property
    def network_id(self):
        return this.run.network

    @property
    def label_index(self):
        return f"A-{str(self.index).zfill(6)}"

    @property
    def label_run_index(self):
        return f"R-{str(self.run.index).zfill(3)}"

