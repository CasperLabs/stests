import typing

from stests.core.cache.utils import encache
from stests.core.cache.utils import encache_singleton
from stests.core.domain import *



@encache
def set_network(network: Network) -> typing.Tuple[typing.List[str], Network]:
    """Encaches domain object: Network.

    :param network: Network domain object instance to be cached.
    
    :returns: Keypath + domain object instance.

    """
    return [
        "network",
        network.name,
    ], network


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
    

@encache
def set_network_node(node: Node) -> typing.Tuple[typing.List[str], Node]:
    """Encaches domain object: Node.
    
    :param node: Node domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        "network-node",
        node.network,
        f"N-{str(node.index).zfill(4)}"
    ], node


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
