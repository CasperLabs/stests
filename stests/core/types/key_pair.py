import enum
import tempfile
import typing
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from stests.core import clx
from stests.core.types.utils import Entity



class KeyEncoding(enum.Enum):
    """Enumeration over set of key encodings.
    
    """
    BYTES = enum.auto()
    HEX = enum.auto()
    PEM = enum.auto()


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
        return Ed25519PrivateKey.from_private_bytes(self.as_bytes).private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )


@dataclass
class PublicKey(Key):
    """A public key used to verify/identify.
    
    """
    @property
    def as_pem(self) -> str:
        """Returns key as pem string."""
        return Ed25519PublicKey.from_public_bytes(self.as_bytes).public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )


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
        
        if not pvk and not pbk::
            pvk, pbk = clx.get_key_pair(clx.KeyEncoding.HEX)

        return KeyPair(PrivateKey(pvk), PublicKey(pbk))
