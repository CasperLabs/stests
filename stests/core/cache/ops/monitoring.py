import typing

from stests.core.cache.model import Item
from stests.core.cache.model import ItemKey
from stests.core.cache.model import SearchKey
from stests.core.cache.model import StoreOperation
from stests.core.cache.model import StorePartition
from stests.core.cache.ops.utils import cache_op
from stests.core.types.chain import Block
from stests.core.types.chain import DeploySummary
from stests.core.types.infra import NetworkIdentifier
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeMonitoringLock


# Cache partition.
_PARTITION = StorePartition.MONITORING

# Cache collections.
COL_BLOCK = "block"
COL_DEPLOY = "deploy"
COL_NODE_LOCK = "node-lock"
COL_EVENT = "event"



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


@cache_op(_PARTITION, StoreOperation.GET_ONE)
def get_block(network_id: NetworkIdentifier, block_hash: str) -> ItemKey:
    """Returns a cached item: Block.
    
    :param network_id: Identifier of network.
    :param block_hash: Hash of a cached block.

    :returns: Key of cached item.

    """
    return ItemKey(
        paths=[
            network_id.name,
            COL_BLOCK,
        ],
        names=[
            "*",
            block_hash,
        ],
    )


@cache_op(_PARTITION, StoreOperation.GET_ONE)
def get_deploy(network_id: NetworkIdentifier, deploy_hash: str) -> ItemKey:
    """Returns a cached item: Deploy.
    
    :param network_id: Identifier of network.
    :param deploy_hash: Hash of a cached deploy.

    :returns: Key of cached item.

    """
    return ItemKey(
        paths=[
            network_id.name,
            COL_DEPLOY,
        ],
        names=[
            "*",
            deploy_hash,
        ],
    )


@cache_op(_PARTITION, StoreOperation.SET_ONE_SINGLETON)
def set_block(block: Block) -> Item:
    """Encaches an item.
    
    :param block: Block instance to be cached.

    :returns: Item to be cached.

    """
    return Item(
        item_key=ItemKey(
            paths=[
                block.network,
                COL_BLOCK,
            ],
            names=[
                block.label_j_rank,
                block.block_hash,
            ],
        ),
        data=block
    )


@cache_op(_PARTITION, StoreOperation.SET_ONE_SINGLETON)
def set_deploy_summary(summary: DeploySummary) -> Item:
    """Encaches an item.
    
    :param summary: Deploy summary instance to be cached.

    :returns: Item to be cached.

    """
    return Item(
        item_key=ItemKey(
            paths=[
                summary.network,
                COL_DEPLOY,
            ],
            names=[
                summary.block_hash,
                summary.deploy_hash,
            ],
        ),
        data=summary
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


@cache_op(_PARTITION, StoreOperation.SET_ONE_SINGLETON)
def set_node_event_info(lock: NodeEventInfo) -> Item:
    """Encaches an item.
    
    :param lock: Lock instance to be cached.

    :returns: Item to be cached.

    """
    return Item(
        item_key=ItemKey(
            paths=[
                lock.network,
                COL_EVENT,
                lock.label_node_index,
            ],
            names=[
                lock.label_event_id,
                lock.label_event_type,
            ],
        ),
        data=lock
    )
