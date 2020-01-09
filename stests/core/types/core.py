from dataclasses import dataclass

from dataclasses_json import dataclass_json



@dataclass_json
@dataclass
class KeyPair():
    """Represents a digital key pair used for identification, signature and verification purposes.
    
    """
    # Private key used for digital signature signing purposes.
    private_key: str

    # Public key used for account addressing & digital signature verification purposes.
    public_key: str


# Set: supported domain types.
TYPESET = {
    KeyPair,
}
