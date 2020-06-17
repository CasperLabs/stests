import dataclasses
import tempfile

from stests.core.utils import crypto



@dataclasses.dataclass
class Key():
    """Represents a digital key pair used for identification, signature and verification purposes.
    
    """
    # Key as hexadecimal format.
    as_hex: str

    @property
    def as_bytes(self) -> bytes:
        """Key as byte array format."""
        return bytes.fromhex(self.as_hex)

    @property
    def as_pem_filepath(self) -> str:
        """Key as a pem file path."""
        tempfile.NamedTemporaryFile
        with tempfile.NamedTemporaryFile("wb", delete=False) as temp_file:
            with open(temp_file.name, "wb") as fstream:
                fstream.write(self.as_pem)
            return temp_file.name


@dataclasses.dataclass
class PrivateKey(Key):
    """A private key used to sign/verify/identify.
    
    """
    @property
    def as_pem(self) -> str:
        """Key as pem string."""
        return crypto.get_pvk_pem_from_bytes(self.as_bytes)


@dataclasses.dataclass
class PublicKey(Key):
    """A public key used to verify/identify.
    
    """
    @property
    def as_pem(self) -> str:
        """Returns key as pem string."""
        return crypto.get_pbk_pem_from_bytes(self.as_bytes)
