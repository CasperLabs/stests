import typing
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey



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


@dataclass_json
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

    @classmethod
    def create(cls, pvk: typing.AnyStr = None):
        """Factory: returns an instance for testing purposes.
        
        """
        pvk = pvk or "a164cfbf6f0797c4894bec5683fb3c715f2acd07c412747db8b91160e9db7c78"

        return PrivateKey(pvk if isinstance(pvk, str) else pvk.hex())


@dataclass_json
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

    @classmethod
    def create(cls, pbk: typing.AnyStr = None):
        """Factory: returns an instance for testing purposes.
        
        """
        pbk = pbk or "ee12b3606431ca201c605409c345427388d54c397386aa513185be6649b4ed61"

        return PublicKey(pbk if isinstance(pbk, str) else pbk.hex())    


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
        return KeyPair(
            PrivateKey.create(pvk),
            PublicKey.create(pbk)
            )
