import typing

from stests.core.cache.enums import StoreOperation
from stests.core.cache.enums import StorePartition
from stests.core.cache.utils import cache_op
from stests.core.domain import *


# Cache collections.
COL_BLOCK = "block"
COL_BLOCK_LOCK = "block-lock"
COL_DEPLOY = "deploy"
COL_STREAM_LOCK = "stream-lock"



@cache_op(StorePartition.MONITORING, StoreOperation.DELETE)
def delete_stream_lock(lock: NodeStreamLock) -> typing.Generator:
    """Deletes astream lock.

    :param ctx: Execution context information.

    :returns: A keypath to be deleted.
    
    """
    return [
        lock.network,
        COL_STREAM_LOCK,
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
        COL_STREAM_LOCK,
        "*",
    ]


@cache_op(StorePartition.MONITORING, StoreOperation.SET_SINGLETON)
def set_block(block: Block) -> typing.Tuple[typing.List[str], Block]:
    """Encaches domain object: Block.
    
    :param block: Block domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        block.network,
        COL_BLOCK,
        f"{str(block.m_rank).zfill(7)}.{block.block_hash}"
    ], block


@cache_op(StorePartition.MONITORING, StoreOperation.LOCK)
def set_block_lock(lock: BlockLock) -> typing.Tuple[typing.List[str], BlockLock]:
    """Encaches a lock: BlockLock.

    :param lock: Information to be locked.

    """
    return [
        lock.network,
        COL_BLOCK_LOCK,
        lock.block_hash,
    ], lock


@cache_op(StorePartition.MONITORING, StoreOperation.SET_SINGLETON)
def set_deploy(deploy: Deploy) -> typing.Tuple[typing.List[str], Deploy]:
    """Encaches domain object: Deploy.
    
    :param block: Deploy domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        deploy.network,
        COL_DEPLOY,
        f"{deploy.block_hash}.{deploy.deploy_hash}"
    ], deploy


@cache_op(StorePartition.MONITORING, StoreOperation.LOCK)
def set_stream_lock(lock: NodeStreamLock) -> typing.Tuple[typing.List[str], NodeStreamLock]:
    """Encaches a lock: NodeStreamLock.

    :param lock: Information to be locked.

    """
    return [
        lock.network,
        COL_STREAM_LOCK,
        lock.lock_index,
    ], lock
