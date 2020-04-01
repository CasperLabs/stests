import typing

from stests.core.cache.enums import StoreOperation
from stests.core.cache.enums import StorePartition
from stests.core.cache.utils import cache_op
from stests.core.domain import *


# Cache collections.
COL_BLOCK = "block"
COL_BLOCK_INFO = "block-info"
COL_BLOCK_LOCK = "block-lock"
COL_DEPLOY = "deploy"
COL_DEPLOY_INFO = "deploy-info"
COL_NODE_LOCK = "node-lock"



@cache_op(StorePartition.MONITORING, StoreOperation.DELETE)
def delete_node_monitor_lock(lock: NodeMonitorLock) -> typing.Generator:
    """Deletes astream lock.

    :param ctx: Execution context information.

    :returns: A keypath to be deleted.
    
    """
    return [
        lock.network,
        COL_NODE_LOCK,
        lock.index_label,
        lock.lock_index,
    ]


@cache_op(StorePartition.MONITORING, StoreOperation.FLUSH)
def flush_stream_locks() -> typing.Generator:
    """Flushes all stream locks.

    :param ctx: Execution context information.

    :returns: A keypath to be deleted.
    
    """
    return [
        "*",
        COL_NODE_LOCK,
        "*",
    ]


@cache_op(StorePartition.MONITORING, StoreOperation.GET_ONE)
def get_block(network_id: NetworkIdentifier, block_hash: str) -> typing.List[str]:
    """Returns domain object: Block.
    
    :param block_hash: Hash of a cached block.

    :returns: Cached block information.

    """
    return [
        network_id.name,
        COL_BLOCK,
        f"*.{block_hash}"
    ]


@cache_op(StorePartition.MONITORING, StoreOperation.GET_ONE)
def get_block_info(network_id: NetworkIdentifier, block_hash: str) -> typing.List[str]:
    """Returns domain object: Block.
    
    :param block_hash: Hash of a cached block.

    :returns: Cached block information.

    """
    return [
        network_id.name,
        COL_BLOCK_INFO,
        f"*.{block_hash}"
    ]


@cache_op(StorePartition.MONITORING, StoreOperation.GET_ONE)
def get_deploy(network_id: NetworkIdentifier, deploy_hash: str) -> typing.List[str]:
    """Returns domain object: Deploy.
    
    :param block_hash: Hash of a cached block.

    :returns: Cached block information.

    """
    return [
        network_id.name,
        COL_DEPLOY,
        f"*.{deploy_hash}"
    ]


@cache_op(StorePartition.MONITORING, StoreOperation.GET_ONE)
def get_deploy_info(network_id: NetworkIdentifier, deploy_hash: str) -> typing.List[str]:
    """Returns domain object: Block.
    
    :param block_hash: Hash of a cached block.

    :returns: Cached block information.

    """
    return [
        network_id.name,
        COL_DEPLOY_INFO,
        f"*.{deploy_hash}"
    ]


@cache_op(StorePartition.MONITORING, StoreOperation.SET_SINGLETON)
def set_block(block: Block) -> typing.Tuple[typing.List[str], Block]:
    """Encaches domain object: Block.
    
    :param block: Block domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    path = [
        block.network,
        COL_BLOCK,
        f"{block.label_m_rank}.{block.block_hash}"
    ]
    
    return path, block


@cache_op(StorePartition.MONITORING, StoreOperation.SET)
def set_block_info(block: Block, block_info: typing.Dict) -> typing.Tuple[typing.List[str], typing.Dict]:
    """Encaches block information queried from a node.
    
    :param block: Block domain object.
    :param block: Block info queried from a node.

    :returns: Keypath + block info.

    """
    path = [
        block.network,
        COL_BLOCK_INFO,
        f"{block.label_m_rank}.{block.block_hash}"
    ]
    
    return path, block_info


@cache_op(StorePartition.MONITORING, StoreOperation.LOCK)
def set_block_lock(lock: BlockLock) -> typing.Tuple[typing.List[str], BlockLock]:
    """Encaches a lock: BlockLock.

    :param lock: Information to be locked.

    """
    path = [
        lock.network,
        COL_BLOCK_LOCK,
        lock.block_hash,
        lock.event_type,
    ]
    
    return path, lock


@cache_op(StorePartition.MONITORING, StoreOperation.SET_SINGLETON)
def set_deploy(block: Block, deploy: Deploy) -> typing.Tuple[typing.List[str], Deploy]:
    """Encaches domain object: Deploy.
    
    :param block: Deploy domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    path = [
        deploy.network,
        COL_DEPLOY,
        f"{block.label_m_rank}.{deploy.block_hash}.{deploy.deploy_hash}"
    ]
    
    return path, deploy


@cache_op(StorePartition.MONITORING, StoreOperation.SET_SINGLETON)
def set_deploy_info(block: Block, deploy: Deploy, deploy_info: typing.Dict) -> typing.Tuple[typing.List[str], typing.Dict]:
    """Encaches deploy information queried from a node.
    
    :param deploy: Deploy domain object.
    :param deploy_info: Deploy info queried from a node.

    :returns: Keypath + deploy info.

    """
    path = [
        deploy.network,
        COL_DEPLOY_INFO,
        f"{block.label_m_rank}.{deploy.block_hash}.{deploy.deploy_hash}"
    ]
    
    return path, deploy_info


@cache_op(StorePartition.MONITORING, StoreOperation.LOCK)
def set_node_monitor_lock(lock: NodeMonitorLock) -> typing.Tuple[typing.List[str], NodeMonitorLock]:
    """Encaches a lock: NodeMonitorLock.

    :param lock: Information to be locked.

    """
    path = [
        lock.network,
        COL_NODE_LOCK,
        lock.index_label,
        lock.lock_index,
    ]
    
    return path, lock
