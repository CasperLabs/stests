import enum


class BrokerMode(enum.Enum):
    """Enumeration over set of broker modes.
    
    """
    SIMULATION = enum.auto()
    MONITORING = enum.auto()
