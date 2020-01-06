from dataclasses import dataclass
from dataclasses_json import dataclass_json



@dataclass_json
@dataclass
class ExecutionContext():
    """Represents contextual information relevant to current execution process.
    
    """
    network_id: str
    generator_id: str
    generator_run: int = 0


@dataclass_json
@dataclass
class KeyPair():
    """Represents a digital key pair used for identification, signature and verification purposes.
    
    """
    private_key: str
    public_key: str


# Set: supported domain types.
TYPESET = {
    ExecutionContext,
    KeyPair
}

