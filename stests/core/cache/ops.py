import enum



class StoreOperation(enum.Enum):
    """Enumeration over types of cache operation.
    
    """
    FLUSH = enum.auto()
    GET = enum.auto()
    GET_SINGLETON = enum.auto()
    INCR = enum.auto()
    LOCK = enum.auto()
    SET = enum.auto()
    SET_SINGLETON = enum.auto()
