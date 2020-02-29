import enum



class StorePartition(enum.Enum):
    """Enumeration over set of types of store partition.
    
    """
    INFRA = enum.auto()
    RUN = enum.auto()
    MONITORING = enum.auto()
