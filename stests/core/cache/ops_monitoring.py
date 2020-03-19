import typing

from stests.core.cache.enums import StoreOperation
from stests.core.cache.enums import StorePartition
from stests.core.cache.utils import cache_op
from stests.core.domain import *
from stests.core.orchestration import StreamLock


# Cache collections.
COL_CONTRACT = "client-contract"
COL_NETWORK = "network"
COL_NODE = "node"



@cache_op(StorePartition.MONITORING, StoreOperation.DELETE)
def delete_stream_lock(lock: StreamLock) -> typing.Generator:
    """Deletes astream lock.

    :param ctx: Execution context information.

    :returns: A keypath to be deleted.
    
    """
    return [
        "stream-lock",
        lock.network,
        lock.lock_index,
    ]
    


@cache_op(StorePartition.MONITORING, StoreOperation.FLUSH)
def flush_stream_locks() -> typing.Generator:
    """Flushes all stream locks.

    :param ctx: Execution context information.

    :returns: A keypath to be deleted.
    
    """
    return [
        "stream-lock",
        "*",
    ]


@cache_op(StorePartition.MONITORING, StoreOperation.SET_SINGLETON)
def set_block(block: Block) -> typing.Tuple[typing.List[str], Block]:
    """Encaches domain object: Block.
    
    :param block: Block domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        "block",
        block.network,
        f"{str(block.m_rank).zfill(7)}.{block.block_hash}"
    ], block


@cache_op(StorePartition.MONITORING, StoreOperation.SET_SINGLETON)
def set_deploy(deploy: Deploy) -> typing.Tuple[typing.List[str], Deploy]:
    """Encaches domain object: Deploy.
    
    :param block: Deploy domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        "deploy",
        deploy.network,
        f"{deploy.block_hash}.{deploy.deploy_hash}"
    ], deploy


@cache_op(StorePartition.MONITORING, StoreOperation.LOCK)
def set_stream_lock(lock: StreamLock) -> typing.Tuple[typing.List[str], StreamLock]:
    """Encaches a lock: StreamLock.

    :param lock: Information to be locked.

    """
    return [
        "stream-lock",
        lock.network,
        lock.lock_index,
    ], lock
