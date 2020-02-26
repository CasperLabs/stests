from dataclasses import dataclass
from dataclasses_json import dataclass_json



@dataclass_json
@dataclass
class RunStepLock:
    """Lock information when executing a run step.
    
    """
    # Associated network.
    network: str

    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: int

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str

    # Step name.
    step: str
