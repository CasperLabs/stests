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


@dataclasses.dataclass
class KeyPair:
    """Represents a digital key pair used for identification, signature and verification purposes.
    
    """
    # Private key used for digital signature signing purposes.
    private_key: PrivateKey

    # Public key used for account addressing & digital signature verification purposes.
    public_key: PublicKey


    @classmethod
    def create(cls, pvk_hex=None, pbk_hex=None):
        """Factory: returns an instance derived from .
        
        """
        if (not pvk_hex and pbk_hex) or (pvk_hex and not pbk_hex):
            raise ValueError("Must either specify both keys or none at all.")
        
        if not pvk_hex and not pbk_hex:
            pvk_hex, pbk_hex = crypto.generate_key_pair(
                crypto.KeyAlgorithm.ED25519,
                crypto.KeyEncoding.HEX
                )

        return cls(PrivateKey(pvk_hex), PublicKey(pbk_hex))

    
    @classmethod
    def create_from_pvk_pem_file(cls, fpath):
        """Factory: returns an instance derived from a private key PEM file.
        
        """
        pvk_hex, pbk_hex = crypto.get_key_pair_from_pvk_pem_file(
            fpath,
            crypto.KeyAlgorithm.ED25519,
            crypto.KeyEncoding.HEX
            )

        return cls.create(pvk_hex, pbk_hex)

