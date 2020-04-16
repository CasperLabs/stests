import random
import typing

from stests.core.cache.enums import StoreOperation
from stests.core.cache.enums import StorePartition
from stests.core.cache.utils import cache_op
from stests.core.domain import *
from stests.core.orchestration import *
from stests.core import factory



# Cache partition.
_PARTITION = StorePartition.INFRA

# Cache collections.
COL_CONTRACT = "client-contract"
COL_NAMED_KEY = "named-key"
COL_NETWORK = "network"
COL_NODE = "node"



@cache_op(_PARTITION, StoreOperation.GET_ONE)
def get_named_key(network: typing.Union[NetworkIdentifier, Network, str], contract_type: ContractType, name: str) -> NamedKey:
    """Decaches domain objects: NamedKey.

    :param network: A pointer to either a network or network identifier.

    :returns: Collection of registered nodes.
    
    """
    try:
        network = network.name
    except AttributeError:
        pass

    return [
        network,
        COL_NAMED_KEY,
        contract_type.name,
        name
    ]


@cache_op(_PARTITION, StoreOperation.GET_MANY)
def get_named_keys(network: typing.Union[NetworkIdentifier, Network, str]) -> typing.List[NamedKey]:
    """Decaches domain objects: NamedKey.

    :param network: A pointer to either a network or network identifier.

    :returns: Collection of registered nodes.
    
    """
    try:
        network = network.name
    except AttributeError:
        pass

    return [
        network,
        COL_NAMED_KEY,
    ]


@cache_op(_PARTITION, StoreOperation.GET)
def get_network(network_id: NetworkIdentifier) -> Network:
    """Decaches domain object: Network.

    :param network_id: A network identifier.

    :returns: A registered network.
    
    """
    return [
        network_id.name,
        COL_NETWORK,
    ]


def get_network_by_ctx(ctx: ExecutionContext) -> Network:
    """Decaches domain object: Network.
    
    :param ctx: Execution context information.

    :returns: A registered network.

    """
    network_id = factory.create_network_id(ctx.network)

    return get_network(network_id)


def get_network_by_name(name: str) -> Network:
    """Decaches domain object: Network.
    
    :param name: Name of a registered network.

    :returns: A registered network.

    """
    return get_network(factory.create_network_id(name))


@cache_op(_PARTITION, StoreOperation.GET)
def get_networks() -> typing.List[Network]:
    """Decaches domain objects: Network.

    :returns: List of registered networks.
    
    """
    return [
        "*",
        COL_NETWORK,
        ]


@cache_op(_PARTITION, StoreOperation.GET)
def get_node(node_id: NodeIdentifier) -> Node:
    """Decaches domain object: Node.
    
    :param node_id: A node identifier.

    :returns: A registered node.

    """
    return [
        node_id.network.name,
        COL_NODE,
        node_id.index_label,
    ]


def get_node_by_network(network: typing.Union[Network, NetworkIdentifier]) -> Node:
    """Decaches domain object: Node.
    
    :param network: A network.

    :returns: A registered node selected at random from a network's nodeset.

    """
    # Pull operational nodeset.
    nodeset = get_nodes_operational(network) 
    if not nodeset:
        raise ValueError(f"Network {network.name} has no registered operational nodes.")

    # Select random node.
    return random.choice(nodeset)
    

def get_node_by_ctx(ctx: ExecutionContext) -> Node:
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


@cache_op(_PARTITION, StoreOperation.GET)
def get_nodes(network: typing.Union[NetworkIdentifier, Network]=None) -> typing.List[Node]:
    """Decaches domain objects: Node.

    :param network: A pointer to either a network or network identifier.

    :returns: Collection of registered nodes.
    
    """
    if network is None:
        return ["*", COL_NODE, "*"]
    else:
        return [
            network.name,
            COL_NODE,
            "N-*"
        ]


def get_nodes_operational(network: typing.Union[NetworkIdentifier, Network]) -> typing.List[Node]:
    """Decaches domain objects: Node (if operational).

    :param network: A pointer to either a network or network identifier.

    :returns: Collection of registered nodes.
    
    """
    nodeset = {i.address: i for i in get_nodes(network) if i.is_operational}

    return list(nodeset.values())


@cache_op(_PARTITION, StoreOperation.SET)
def set_named_key(named_key: NamedKey) -> typing.Tuple[typing.List[str], NamedKey]:
    """Encaches domain object: NamedKey.

    :param network: NamedKey domain object instance to be cached.
    
    :returns: Keypath + domain object instance.

    """
    path = [
        named_key.network,
        COL_NAMED_KEY,
        named_key.contract_type.name,
        named_key.name
    ]

    return path, named_key


@cache_op(_PARTITION, StoreOperation.SET)
def set_network(network: Network) -> typing.Tuple[typing.List[str], Network]:
    """Encaches domain object: Network.

    :param network: Network domain object instance to be cached.
    
    :returns: Keypath + domain object instance.

    """
    path = [
        network.name,
        COL_NETWORK,
    ]

    return path, network


@cache_op(_PARTITION, StoreOperation.SET)
def set_node(node: Node) -> typing.Tuple[typing.List[str], Node]:
    """Encaches domain object: Node.
    
    :param node: Node domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    path = [
        node.network,
        COL_NODE,
        node.index_label,
    ]

    return path, node
