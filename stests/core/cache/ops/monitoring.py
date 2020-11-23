from stests.core.cache.model import Item
from stests.core.cache.model import ItemKey
from stests.core.cache.model import StoreOperation
from stests.core.cache.model import StorePartition
from stests.core.cache.ops.utils import cache_op
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeMonitoringLock


# Cache collections.
COL_BLOCK = "block"
COL_DEPLOY = "deploy"
COL_EVENT = "event"
COL_NODE_LOCK = "node-lock"


@cache_op(StorePartition.MONITORING_LOCKS, StoreOperation.DELETE_ONE)
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


@cache_op(StorePartition.MONITORING, StoreOperation.SET_ONE_SINGLETON)
def set_block(network: str, block_hash: str) -> Item:
    """Encaches an item.
    
    :param summary: Block summary instance to be cached.

    :returns: Item to be cached.

    """
    return Item(
        item_key=ItemKey(
            paths=[
                network,
                COL_BLOCK,
            ],
            names=[
                block_hash,
            ],
        ),
        data={
            "block_hash": block_hash,
            "network": network,
        }
    )


@cache_op(StorePartition.MONITORING, StoreOperation.SET_ONE_SINGLETON)
def set_deploy(network: str, block_hash: str, deploy_hash: str) -> Item:
    """Encaches an item.
    
    :param summary: Deploy summary instance to be cached.

    :returns: Item to be cached.

    """
    return Item(
        item_key=ItemKey(
            paths=[
                network,
                COL_DEPLOY,
            ],
            names=[
                block_hash,
                deploy_hash,
            ],
        ),
        data={
            "block_hash": block_hash,
            "deploy_hash": deploy_hash,
            "network": network,
        }
    )


@cache_op(StorePartition.MONITORING, StoreOperation.SET_ONE_SINGLETON)
def set_node_event_info(info: NodeEventInfo) -> Item:
    """Encaches an item.
    
    :param info: Node event information.

    :returns: Item to be cached.

    """
    return Item(
        item_key=ItemKey(
            paths=[
                info.network,
                COL_EVENT,
                info.label_node_index,
            ],
            names=[
                info.label_event_id,
                info.label_event_type,
            ],
        ),
        data=info
    )


@cache_op(StorePartition.MONITORING_LOCKS, StoreOperation.SET_ONE_SINGLETON)
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
