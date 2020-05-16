import typing

from stests.core.cache.model import Item
from stests.core.cache.model import ItemKey
from stests.core.cache.model import StoreOperation
from stests.core.cache.model import StorePartition
from stests.core.cache.ops.utils import cache_op
from stests.core.types.infra import NodeMonitoringLock


# Cache partition.
_PARTITION = StorePartition.MONITORING_LOCKS

# Cache collections.
COL_NODE_LOCK = "node-lock"



@cache_op(_PARTITION, StoreOperation.DELETE_ONE)
def delete_node_monitor_lock(lock: NodeMonitoringLock) -> ItemKey:
    """Deletes a lock over a node monitor.

    :param lock: Lock information.

    :returns: Key of locked item.
    
    """
    return ItemKey(
        paths=[
            lock.network,
            COL_NODE_LOCK,
            lock.label_node_index,
        ],
        names=[
            lock.lock_index,
        ],
    )


@cache_op(_PARTITION, StoreOperation.SET_ONE_SINGLETON)
def set_node_monitor_lock(lock: NodeMonitoringLock) -> Item:
    """Encaches an item.
    
    :param lock: Lock instance to be cached.

    :returns: Item to be cached.

    """
    return Item(
        item_key=ItemKey(
            paths=[
                lock.network,
                COL_NODE_LOCK,
                lock.label_node_index,
            ],
            names=[
                lock.lock_index,
            ],
        ),
        data=lock
    )
