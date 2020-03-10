import random
import typing

from stests.core.cache.enums import StoreOperation
from stests.core.cache.enums import StorePartition
from stests.core.cache.utils import cache_op
from stests.core.domain import *
from stests.core.orchestration import *
from stests.core.utils import factory



@cache_op(StorePartition.INFRA, StoreOperation.GET)
def get_network(network_id: NetworkIdentifier) -> Network:
    """Decaches domain object: Network.

    :param network_id: A network identifier.

    :returns: A registered network.
    
    """
    return [
        "network",
        network_id.name
    ]


def get_network_by_name(name: str) -> Network:
    """Decaches domain object: Network.
    
    :param name: Name of a registered network.

    :returns: A registered network.

    """
    return get_network(factory.create_network_id(name))


@cache_op(StorePartition.INFRA, StoreOperation.GET)
def get_networks() -> typing.List[Network]:
    """Decaches domain objects: Network.

    :returns: List of registered networks.
    
    """
    return ["network", "*"]


@cache_op(StorePartition.INFRA, StoreOperation.GET)
def get_node(node_id: NodeIdentifier) -> Node:
    """Decaches domain object: Node.
    
    :param node_id: A node identifier.

    :returns: A registered node.

    """
    return [
        "node",
        node_id.network.name,
        f"N-{str(node_id.index).zfill(4)}"
    ]


def get_node_by_network_id(network_id: NetworkIdentifier) -> Node:
    """Decaches domain object: Node.
    
    :param network_id: A network identifier.

    :returns: A registered node selected at random from a network's nodeset.

    """
    # Pull operational nodeset.
    nodeset = get_nodes_operational(network_id) 
    if not nodeset:
        raise ValueError(f"Network {network_id.name} has no registered operational nodes.")

    # Select random node.
    return random.choice(nodeset)
    

def get_node_by_run_context(ctx: ExecutionContext) -> Node:
    """Decaches domain object: Node.
    
    :param ctx: Execution context information.

    :returns: A registered node.

    """
    # Pull operational nodes.
    network_id = factory.create_network_id(ctx.network)
    nodeset = get_nodes_operational(network_id)
    if not nodeset:
        raise ValueError(f"Network {network_id.name} has no registered operational nodes.")
    
    # Select random if node index unspecified.
    if ctx.node_index <= 0 or ctx.node_index is None:
        return random.choice(nodeset)

    # Select specific with fallback to random.
    try:
        return nodeset[ctx.node_index - 1]
    except IndexError:
        return random.choice(nodeset)


@cache_op(StorePartition.INFRA, StoreOperation.GET)
def get_nodes(network: typing.Union[NetworkIdentifier, Network]=None) -> typing.List[Node]:
    """Decaches domain objects: Node.

    :param network: A pointer to either a network or network identifier.

    :returns: Collection of registered nodes.
    
    """
    if network is None:
        return ["node", "*"]
    else:
        return [
            "node",
            network.name,
            "N-*"
        ]


def get_nodes_operational(network: typing.Union[NetworkIdentifier, Network]=None) -> typing.List[Node]:
    """Decaches domain objects: Node (if operational).

    :param network: A pointer to either a network or network identifier.

    :returns: Collection of registered nodes.
    
    """
    return [i for i in get_nodes(network) if i.is_operational]


@cache_op(StorePartition.INFRA, StoreOperation.SET)
def set_network(network: Network) -> typing.Tuple[typing.List[str], Network]:
    """Encaches domain object: Network.

    :param network: Network domain object instance to be cached.
    
    :returns: Keypath + domain object instance.

    """
    return [
        "network",
        network.name,
    ], network


@cache_op(StorePartition.INFRA, StoreOperation.SET)
def set_node(node: Node) -> typing.Tuple[typing.List[str], Node]:
    """Encaches domain object: Node.
    
    :param node: Node domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        "node",
        node.network,
        f"N-{str(node.index).zfill(4)}"
    ], node
