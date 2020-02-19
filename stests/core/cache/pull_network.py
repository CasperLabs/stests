import random
import typing

from stests.core.cache.utils import decache
from stests.core.domain import Network
from stests.core.domain import NetworkIdentifier
from stests.core.domain import Node
from stests.core.domain import NodeIdentifier
from stests.core.utils import factory



@decache
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


@decache
def get_networks() -> typing.List[Network]:
    """Decaches domain objects: Network.

    :returns: List of registered networks.
    
    """
    return ["network", "*"]


@decache
def get_node(node_id: NodeIdentifier) -> Node:
    """Decaches domain object: Node.
    
    :param node_id: A node identifier.

    :returns: A registered node.

    """
    return [
        "network-node",
        node_id.network.name,
        f"N-{str(node_id.index).zfill(4)}"
    ]


def get_node_by_network_id(network_id: NetworkIdentifier) -> Node:
    """Decaches domain object: Node.
    
    :param network_id: A network identifier.

    :returns: A registered node selected at random from a network's nodeset.

    """
    # Pull nodeset.
    nodeset = get_nodes(network_id) 
    if not nodeset:
        raise ValueError(f"Network {network_id.name} has no registered nodes.")
    
    # Select random node.
    return random.choice(nodeset)
    

@decache
def get_nodes(network_id: NetworkIdentifier=None) -> typing.List[Node]:
    """Decaches domain objects: Node.

    :param network_id: A network identifier.

    :returns: Collection of registered nodes.
    
    """
    if network_id is None:
        return ["network-node", "*"]
    else:
        return [
            "network-node",
            network_id.name,
            "N-*"
        ]
