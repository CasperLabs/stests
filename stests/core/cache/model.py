import enum
import json
import typing

from stests.core.utils import encoder



class CacheItemKey():
    def __init__(self, paths: typing.List[str], names: typing.List[str]):
        self.path = ":".join([str(i) for i in paths])
        self.name = ".".join([str(i) for i in names])
    
    @property
    def key(self) -> str:
        return f"{self.path}:{self.name}"


class CacheItem():
    def __init__(self, item_key: CacheItemKey, data: typing.Any):
        self.key = item_key.key
        self.data = data

    @property
    def data_as_json(self):
        return json.dumps(encoder.encode(self.data), indent=4)


class CacheSearchKey():
    def __init__(self, paths: typing.List[str], wildcard="*"):
        self.key = f"{':'.join([str(i) for i in paths])}{wildcard}"


class CacheDecrementKey(CacheItemKey):
    def __init__(self, paths: typing.List[str], names: typing.List[str], amount: int):
        super().__init__(paths, names)
        self.amount = amount


class CacheIncrementKey(CacheItemKey):
    def __init__(self, paths: typing.List[str], names: typing.List[str], amount: int):
        super().__init__(paths, names)
        self.amount = amount


class StoreOperation(enum.Enum):
    """Enumeration over types of cache operation.
    
    """
    # Atomically decrement a counter.
    DECR = enum.auto()

    # Atomically decrement a counter.
    DECR_ONE = enum.auto()

    # Delete a key.
    DELETE = enum.auto()

    # Delete a key.
    DELETE_ONE = enum.auto()

    # Flush a key set.
    FLUSH = enum.auto()

    # Flush a key set.
    FLUSH_MANY = enum.auto()
    
    # Get cached item.
    GET = enum.auto()

    # Get count of cached item.
    GET_COUNT = enum.auto()

    # Get count of cached item.
    GET_COUNT_ONE = enum.auto()

    # Get count of cached items.
    GET_COUNT_MANY = enum.auto()

    # Get count of matched cache item.
    GET_COUNT_MATCHED = enum.auto()

    # Get list of counts.
    GET_COUNTS = enum.auto()

    # Get a single cached item.
    GET_ONE = enum.auto()

    # Get a single cached item from a collection.
    GET_ONE_FROM_MANY = enum.auto()

    # Get a collection of cached items.
    GET_MANY = enum.auto()

    # Atomically increment a counter.
    INCR = enum.auto()

    # Atomically set a lock.
    LOCK = enum.auto()

    # Atomically set a lock.
    LOCK_ONE = enum.auto()

    # Set an item.
    SET = enum.auto()

    # Set an item.
    SET_ONE = enum.auto()

    # Set cached item plus flag indicating whether it already was cached.
    SET_ONE_SINGLETON = enum.auto()
    
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
