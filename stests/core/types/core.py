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


    @staticmethod
    def create():
        """Factory: returns an instance for testing purposes.
        
        """
        return KeyPair(
            "a164cfbf6f0797c4894bec5683fb3c715f2acd07c412747db8b91160e9db7c78", 
            "ee12b3606431ca201c605409c345427388d54c397386aa513185be6649b4ed61"
            )


# Set: supported domain types.
CLASSES = {
    KeyPair,
}
