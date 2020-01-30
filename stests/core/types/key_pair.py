import tempfile
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.types.utils import Entity
from stests.core.utils import crypto



@dataclass_json
@dataclass
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


@dataclass
class PrivateKey(Key):
    """A private key used to sign/verify/identify.
    
    """
    @property
    def as_pem(self) -> str:
        """Key as pem string."""
        return crypto.get_private_key_pem(self.as_bytes)


@dataclass
class PublicKey(Key):
    """A public key used to verify/identify.
    
    """
    @property
    def as_pem(self) -> str:
        """Returns key as pem string."""
        return crypto.get_public_key_pem(self.as_bytes)


@dataclass_json
@dataclass
class KeyPair():
    """Represents a digital key pair used for identification, signature and verification purposes.
    
    """
    # Private key used for digital signature signing purposes.
    private_key: PrivateKey

    # Public key used for account addressing & digital signature verification purposes.
    public_key: PublicKey

    @classmethod
    def create(cls, pvk=None, pbk=None):
        """Factory: returns an instance for testing purposes.
        
        """
        if (not pvk and pbk) or (pvk and not pbk):
            raise ValueError("Must either specify both keys or none at all.")
        
        if not pvk and not pbk:
            pvk, pbk = crypto.get_key_pair(crypto.KeyEncoding.HEX)

        return KeyPair(PrivateKey(pvk), PublicKey(pbk))
