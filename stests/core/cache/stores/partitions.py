import enum



class StorePartition(enum.Enum):
    """Enumeration over set of types of store partition.
    
    """
    INFRA = enum.auto()
    GENERATOR = enum.auto()
    MONITORING = enum.auto()
