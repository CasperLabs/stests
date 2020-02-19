import random
import typing

from stests.core.cache.utils import decache
from stests.core.cache.identifiers import NetworkIdentifier
from stests.core.cache.identifiers import NodeIdentifier
from stests.core.domain import Network
from stests.core.domain import Node
from stests.core.domain import RunContext
from stests.core.utils import factory



@decache
def get_network(network_id: NetworkIdentifier) -> Network:
    """Decaches domain object: Network.
    
    """
    return [
        "network",
        network_id.name
    ]


@decache
def get_networks() -> typing.List[Network]:
    """Decaches domain objects: Network.
    
    """
    return ["network", "*"]


@decache
def get_node(node_id: NodeIdentifier) -> Node:
    """Decaches domain object: Node.
    
    """
    return [
        "network-node",
        node_id.network.name,
        f"N-{str(node_id.index).zfill(4)}"
    ]


@decache
def get_nodes(network_id: NetworkIdentifier=None) -> typing.List[Node]:
    """Decaches domain objects: Node.
    
    """
    if network_id is None:
        return ["network-node", "*"]
    else:
        return [
            "network-node",
            network_id.name,
            "N-*"
        ]


def get_network_by_ctx(ctx: RunContext) -> Network:
    """Decaches domain object: Network.
    
    """
    network_id = factory.create_network_id(ctx.network_name)

    return get_network(network_id)


def get_network_by_name(name: str) -> Network:
    """Decaches domain object: Network.
    
    """
    network_id = factory.create_network_id(name)

    return get_network(network_id)


def get_node_by_ctx(ctx: RunContext) -> Node:
    """Decaches domain object: Node.
    
    """
    # Pull nodes.
    network_id = factory.create_network_id(ctx.network_name)
    nodes = get_nodes(network_id) 
    if not nodes:
        raise ValueError(f"Network {network_id.name} has no registered nodes.")
    
    # Select random if node index unspecified.
    if ctx.node_index <= 0 or ctx.node_index is None:
        return random.choice(nodes)

    # Select specific with fallback to random.
    try:
        return nodes[ctx.node_index - 1]
    except IndexError:
        return random.choice(nodes)


def get_node_by_network_id(network_id: NetworkIdentifier) -> Node:
    """Decaches domain object: Node.
    
    """
    # Pull nodes.
    nodes = get_nodes(network_id) 
    if not nodes:
        raise ValueError(f"Network {network_id.name} has no registered nodes.")
    
    # Select random node.
    return random.choice(nodes)