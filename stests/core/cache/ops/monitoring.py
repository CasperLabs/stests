from stests.core.cache.model import Item
from stests.core.cache.model import ItemKey
from stests.core.cache.model import StoreOperation
from stests.core.cache.model import StorePartition
from stests.core.cache.ops.utils import cache_op
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeMonitoringLock
from stests.events import EventType



# Cache collections.
COL_BLOCK = "block"
COL_DEPLOY = "deploy"
COL_EVENT = "event"
COL_NODE_LOCK = "node-lock"

# Cache collection item expiration times.
EXPIRATION_COL_BLOCK = 300
EXPIRATION_COL_DEPLOY = 300
EXPIRATION_COL_EVENT = 300


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
def set_block(info: NodeEventInfo) -> Item:
    """Encaches an item.
    
    :param info: Node event information.

    :returns: Item to be cached.

    """
    return Item(
        item_key=ItemKey(
            paths=[
                info.network,
                COL_BLOCK,
            ],
            names=[
                info.block_hash,
            ],
        ),
        data={
            "block_hash": info.block_hash,
            "network": info.network,
        },
        expiration=EXPIRATION_COL_BLOCK
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
        },
        expiration=EXPIRATION_COL_DEPLOY
    )


@cache_op(StorePartition.MONITORING, StoreOperation.SET_ONE_SINGLETON)
def set_node_event_info(info: NodeEventInfo) -> Item:
    """Encaches an item.
    
    :param info: Node event information.

    :returns: Item to be cached.

    """
    if info.event_type in (
        EventType.MONIT_CONSENSUS_FINALITY_SIGNATURE,
        EventType.MONIT_BLOCK_FINALIZED,
        EventType.MONIT_BLOCK_ADDED,
        ):
        names = [
            info.block_hash,
        ]
    elif info.event_type == EventType.MONIT_DEPLOY_PROCESSED:
        names = [
            info.block_hash,
            info.deploy_hash,
        ]
    else:
        names=[]

    return Item(
        item_key=ItemKey(
            paths=[
                info.network,
                COL_EVENT,
                info.event_type.name[6:],
            ],
            names=names,
        ),
        data=info,
        expiration=EXPIRATION_COL_EVENT
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
