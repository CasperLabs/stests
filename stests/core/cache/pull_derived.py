import random
import typing

from stests.core.cache.identifiers import NetworkIdentifier
from stests.core.cache.pull import get_account
from stests.core.cache.pull import get_network
from stests.core.cache.pull import get_nodes
from stests.core.domain import Account
from stests.core.domain import Network
from stests.core.domain import Node
from stests.core.domain import RunContext
from stests.core.utils import factory



def get_account_by_ctx(ctx: RunContext, index: int) -> Account:
    """Decaches domain object: Account.
    
    """
    account_id = factory.create_account_id(
        index,
        ctx.network_name,
        ctx.run_index,
        ctx.run_type
        )

    return get_account(account_id)


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
