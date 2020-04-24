import enum



class StoreOperation(enum.Enum):
    """Enumeration over types of cache operation.
    
    """
    # Atomically decrement a counter.
    DECR = enum.auto()

    # Delete a key.
    DELETE = enum.auto()

    # Flush a key set.
    FLUSH = enum.auto()
    
    # Get cached item.
    GET = enum.auto()

    # Get count of cached item.
    GET_COUNT = enum.auto()

    # Get count of matched cache item.
    GET_COUNT_MATCHED = enum.auto()

    # Get list of counts.
    GET_COUNTS = enum.auto()

    # Get a single cached item.
    GET_ONE = enum.auto()

    # Get a collection of cached items.
    GET_MANY = enum.auto()

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
