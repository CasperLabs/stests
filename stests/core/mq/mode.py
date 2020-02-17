import enum


class BrokerMode(enum.Enum):
    """Enumeration over set of broker modes.
    
    """
    ACTORS = enum.auto()
    MONITORS = enum.auto()
