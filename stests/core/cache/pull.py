import typing

from stests.core.cache.keyspace import get_key
from stests.core.cache.utils import decache
from stests.core.cache.identifiers import NetworkIdentifier
from stests.core.cache.identifiers import NodeIdentifier
from stests.core.domain import Account
from stests.core.domain import AccountType
from stests.core.domain import Network
from stests.core.domain import Node
from stests.core.domain import RunContext
from stests.core.utils import factory



@decache
def get_account(ctx: RunContext, account_type: AccountType, account_index: int) -> Account:
    """Decaches domain object: Account.
    
    """
    key = f"{get_key(ctx)}:"
    zfill = 6 if obj.typeof == AccountType.USER else 2
    key += f"accounts:{account_type.name}:{str(account_index).zfill(zfill)}"

    return key


@decache
def get_network(network_id: NetworkIdentifier) -> Network:
    """Decaches domain object: Network.
    
    """
    return get_key(network_id)


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


@decache
def get_ctx_node(ctx: RunContext) -> Node:
    """Decaches domain object: Node.
    
    """
    # if ctx.node_index == 0:
    #     node_index = 1
    # else:
    # TODO: randomize if node index = 0.
    key = f"global.network:{network_id.name}"

    return key


@decache
def get_nodes(network_id: NetworkIdentifier) -> typing.List[Node]:
    """Decaches domain objects: Node.
    
    """
    return get_key((network_id, typing.List[Node]))


@decache
def get_run(ctx: RunContext) -> RunContext:
    """Decaches domain object: RunContext.
    
    """
    raise NotImplementedError()
    key = f"{ctx.network_id.name}.{ctx.run_type}:R-{str(ctx.run_index).zfill(3)}"

    return key
