import typing

from stests.core.cache.enums import StoreOperation
from stests.core.cache.enums import StorePartition
from stests.core.cache.utils import cache_op
from stests.core.domain import *



@cache_op(StorePartition.MONITORING, StoreOperation.FLUSH)
def flush_by_network(network_id: NetworkIdentifier) -> typing.Generator:
    """Flushes network specific monitoring information.

    :param network_id: A network identifier.

    :returns: A generator of keypaths to be flushed.
    
    """
    yield ["block", network_id.name, "*"]
    yield ["deploy", network_id.name, "*"]


@cache_op(StorePartition.MONITORING, StoreOperation.SET_SINGLETON)
def set_network_block(block: Block) -> typing.Tuple[typing.List[str], Block]:
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
def set_network_deploy(deploy: Deploy) -> typing.Tuple[typing.List[str], Deploy]:
    """Encaches domain object: Deploy.
    
    :param block: Deploy domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        "deploy",
        deploy.network,
        f"{deploy.block_hash}.{deploy.deploy_hash}"
    ], deploy
