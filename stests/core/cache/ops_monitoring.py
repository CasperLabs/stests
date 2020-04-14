import typing

from stests.core.cache.enums import StoreOperation
from stests.core.cache.enums import StorePartition
from stests.core.cache.utils import cache_op
from stests.core.domain import *


# Cache collections.
COL_BLOCK = "block"
COL_DEPLOY = "deploy"
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


@cache_op(StorePartition.MONITORING, StoreOperation.SET_SINGLETON)
def set_block(block: Block) -> typing.Tuple[typing.List[str], Block]:
    """Encaches domain object: Block.
    
    :param block: Block domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    path = [
        block.network,
        COL_BLOCK,
        f"{block.label_j_rank}.{block.block_hash}"
    ]
    
    return path, block


@cache_op(StorePartition.MONITORING, StoreOperation.SET_SINGLETON)
def set_deploy(deploy: Deploy) -> typing.Tuple[typing.List[str], Deploy]:
    """Encaches domain object: Deploy.
    
    :param block: Deploy domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    path = [
        deploy.network,
        COL_DEPLOY,
        f"{deploy.block_hash}.{deploy.deploy_hash}"
    ]
    
    return path, deploy


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
