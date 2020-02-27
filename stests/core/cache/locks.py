from dataclasses import dataclass



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
