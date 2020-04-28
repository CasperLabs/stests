import typing

from stests.core.cache.model import CacheItem
from stests.core.cache.model import CacheItemKey
from stests.core.cache.model import CacheSearchKey
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
def delete_node_monitor_lock(lock: NodeMonitoringLock) -> CacheItemKey:
    """Deletes astream lock.

    :param ctx: Execution context information.

    :returns: A keypath to be deleted.
    
    """
    return CacheItemKey(
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
def get_block(network_id: NetworkIdentifier, block_hash: str) -> CacheItemKey:
    """Returns domain object: Block.
    
    :param block_hash: Hash of a cached block.

    :returns: Cached block information.

    """
    return CacheItemKey(
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
def get_deploy(network_id: NetworkIdentifier, deploy_hash: str) -> CacheItemKey:
    """Returns domain object: Deploy.
    
    :param deploy_hash: Hash of a cached deploy.

    :returns: Cached deploy information.

    """
    return CacheItemKey(
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
def set_block(block: Block) -> CacheItem:
    """Encaches domain object: Block.
    
    :param block: Block domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return CacheItem(
        item_key=CacheItemKey(
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
def set_deploy_summary(summary: DeploySummary) -> CacheItem:
    """Encaches domain object: DeploySummary.
    
    :param summary: Deploy summary domain object instance to be cached.
    :returns: Keypath + domain object instance.

    """
    return CacheItem(
        item_key=CacheItemKey(
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


@cache_op(_PARTITION, StoreOperation.LOCK_ONE)
def set_node_monitor_lock(lock: NodeMonitoringLock) -> CacheItem:
    """Encaches a lock: NodeMonitoringLock.

    :param lock: Information to be locked.

    """
    return CacheItem(
        item_key=CacheItemKey(
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


@cache_op(_PARTITION, StoreOperation.LOCK_ONE)
def set_node_event_info(lock: NodeEventInfo) -> CacheItem:
    """Encaches domain object: NodeEventInfo.
    
    :param block: Node event information to be cached.

    :returns: Keypath + domain object instance.

    """
    return CacheItem(
        item_key=CacheItemKey(
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
