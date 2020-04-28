import enum
import json
import typing

from stests.core.utils import encoder



class ItemKey():
    """A key of an encached item.
    
    """
    def __init__(self, paths: typing.List[str], names: typing.List[str]):
        self.path = ":".join([str(i) for i in paths])
        self.name = ".".join([str(i) for i in names])
    
    @property
    def key(self) -> str:
        return f"{self.path}:{self.name}"


class Item():
    """An item to be encached alongside it's key.
    
    """
    def __init__(self, item_key: ItemKey, data: typing.Any):
        self.key = item_key.key
        self.data = data

    @property
    def data_as_json(self):
        return json.dumps(encoder.encode(self.data), indent=4)


class CountDecrementKey(ItemKey):
    """A key used to decrement a counter.
    
    """
    def __init__(self, paths: typing.List[str], names: typing.List[str], amount: int):
        super().__init__(paths, names)
        self.amount = amount


class CountIncrementKey(ItemKey):
    """A key used to increment a counter.
    
    """
    def __init__(self, paths: typing.List[str], names: typing.List[str], amount: int):
        super().__init__(paths, names)
        self.amount = amount
        

class SearchKey():
    """A key used to perform a cache search.
    
    """
    def __init__(self, paths: typing.List[str], wildcard="*"):
        self.key = f"{':'.join([str(i) for i in paths])}{wildcard}"


class StoreOperation(enum.Enum):
    """Enumeration over types of cache operation.
    
    """
    # Atomically increment a counter.
    COUNTER_INCR = enum.auto()

    # Atomically decrement a counter.
    COUNTER_DECR = enum.auto()

    # Delete a key.
    DELETE_ONE = enum.auto()

    # Flush a key set.
    DELETE_MANY = enum.auto()
    
    # Get count of matched cache item.
    GET_COUNT = enum.auto()

    # Get value of a cached counter.
    GET_COUNTER_ONE = enum.auto()

    # Get value of many cached counters.
    GET_COUNTER_MANY = enum.auto()

    # Get a single cached item.
    GET_ONE = enum.auto()

    # Get a single cached item from a collection.
    GET_ONE_FROM_MANY = enum.auto()

    # Get a collection of cached items.
    GET_MANY = enum.auto()

    # Set an item.
    SET_ONE = enum.auto()

    # Set cached item plus flag indicating whether it already was cached.
    SET_ONE_SINGLETON = enum.auto()


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
