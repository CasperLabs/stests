import dataclasses
import typing

from stests.core import crypto
from stests.core.types.chain.enums import AccountType



@dataclasses.dataclass
class Account:
    """A non-designated account that maps to an address upon target chain.
    
    """
    # On-chain account identifier.
    account_id: str

    # Numerical index to distinguish between multiple accounts within same run.
    key_algo: str

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
    def account_id_as_bytes(self):
        return bytes.fromhex(self.account_id)

    @property
    def account_hash(self):
        return crypto.get_hash(
            self.account_id_as_bytes,
            algo=crypto.HashAlgorithm.BLAKE2B,
            encoding=crypto.HashEncoding.HEX,
            )

    @property
    def is_run_account(self):
        return self.run_index is not None

    @property
    def label_index(self):
        return f"A-{str(self.index).zfill(6)}"

    @property
    def label_run_index(self):
        return f"R-{str(self.run_index).zfill(3)}"

    def get_private_key_pem_filepath(self):
        """Returns path to associated pem file.
        
        """
        return crypto.get_pvk_pem_file_from_bytes(
            bytes.fromhex(self.private_key),
            crypto.KeyAlgorithm[self.key_algo],
            )


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

