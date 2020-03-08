import enum



class StoreOperation(enum.Enum):
    """Enumeration over types of cache operation.
    
    """
    # Flush cache keys.
    FLUSH = enum.auto()

    # Get cached item.
    GET = enum.auto()

    # Get count of cached item.
    GET_COUNT = enum.auto()

    # Atomically increment a counter.
    INCR = enum.auto()

    # Atomically set a lock.
    LOCK = enum.auto()

    # Set an item.
    SET = enum.auto()

    # Set cached item plus flag indicating whether it already was cached.
    SET_SINGLETON = enum.auto()


class StorePartition(enum.Enum):
    """Enumeration over set of types of store partition.
    
    """
    # Infrastructure.
    INFRA = enum.auto()

    # Chain monitoring.
    MONITORING = enum.auto()

    # Workflow orchestration
    ORCHESTRATION = enum.auto()

    # Workflow state
    STATE = enum.auto()
