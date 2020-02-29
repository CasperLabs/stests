import typing

from stests.core.cache.enums import StoreOperation
from stests.core.cache.enums import StorePartition
from stests.core.cache.utils import cache_op
from stests.core.cache.utils import encache
from stests.core.cache.utils import encache_singleton
from stests.core.domain import *



@cache_op(StorePartition.MONITORING, StoreOperation.SET_SINGLETON)
@encache_singleton
def set_network_block(block: Block) -> typing.Tuple[typing.List[str], Block]:
    """Encaches domain object: Block.
    
    :param block: Block domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        "network-block",
        block.network,
        f"{str(block.m_rank).zfill(7)}.{block.block_hash}"
    ], block


@cache_op(StorePartition.MONITORING, StoreOperation.SET_SINGLETON)
@encache_singleton
def set_network_deploy(deploy: Deploy) -> typing.Tuple[typing.List[str], Deploy]:
    """Encaches domain object: Deploy.
    
    :param block: Deploy domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        "network-deploy",
        deploy.network,
        f"{deploy.block_hash}.{deploy.deploy_hash}"
    ], deploy
