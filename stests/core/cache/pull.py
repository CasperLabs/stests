import random
import typing

from stests.core.cache.keyspace import get_key
from stests.core.cache.utils import decache
from stests.core.cache.identifiers import AccountIdentifier
from stests.core.cache.identifiers import NetworkIdentifier
from stests.core.cache.identifiers import NodeIdentifier
from stests.core.domain import Account
from stests.core.domain import AccountType
from stests.core.domain import Network
from stests.core.domain import Node
from stests.core.domain import RunContext
from stests.core.utils import factory




@decache
def get_account(account_id: AccountIdentifier) -> Account:
    """Decaches domain object: Account.
    
    """
    return get_key(account_id)


def get_account_by_ctx(ctx: RunContext, index: int) -> Account:
    """Decaches domain object: Account.
    
    """
    network_id = factory.create_network_id(ctx.network_name)
    run_id = factory.create_run_id(network_id, ctx.run_index, ctx.run_type)
    account_id = AccountIdentifier(
        index=index,
        run=run_id
    )

    return get_account(account_id)


@decache
def get_network(network_id: NetworkIdentifier) -> Network:
    """Decaches domain object: Network.
    
    """
    return get_key(network_id)


def get_network_by_ctx(ctx: RunContext) -> Network:
    """Decaches domain object: Network.
    
    """
    network_id = factory.create_network_id(ctx.network_name)

    return get_network(network_id)


def get_network_by_name(name: str) -> Network:
    """Decaches domain object: Network.
    
    """
    return get_network(factory.create_network_id(name))


@decache
def get_networks() -> typing.List[Network]:
    """Decaches domain objects: Network.
    
    """
    return get_key(typing.List[Network])


@decache
def get_node(node_id: NodeIdentifier) -> Node:
    """Decaches domain object: Node.
    
    """
    return get_key(node_id)


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


@decache
def get_nodes(network_id: NetworkIdentifier) -> typing.List[Node]:
    """Decaches domain objects: Node.
    
    """
    return get_key((network_id, typing.List[Node]))


def get_node_at_random(network_id: NetworkIdentifier):
    return random.choice(get_nodes(network_id))


@decache
def get_run(ctx: RunContext) -> RunContext:
    """Decaches domain object: RunContext.
    
    """
    raise NotImplementedError()
    key = f"{ctx.network_id.name}.{ctx.run_type}:R-{str(ctx.run_index).zfill(3)}"

    return key
