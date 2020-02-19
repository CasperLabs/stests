import random
import typing

from stests.core.cache.pull_network import get_network
from stests.core.cache.pull_network import get_nodes
from stests.core.cache.utils import decache
from stests.core.domain import Account
from stests.core.domain import AccountIdentifier
from stests.core.domain import Network
from stests.core.domain import Node
from stests.core.domain import NodeStatus
from stests.core.domain import RunContext
from stests.core.utils import factory



@decache
def get_account(account_id: AccountIdentifier) -> Account:
    """Decaches domain object: Account.

    :param account_id: An account identifier.

    :returns: A cached account.

    """
    run = account_id.run

    return [
        "run-account",
        run.network.name,
        run.type,
        f"R-{str(run.index).zfill(3)}",
        f"{str(account_id.index).zfill(6)}"
    ]


def get_run_account(ctx: RunContext, index: int) -> Account:
    """Decaches domain object: Account.
    
    :param ctx: Generator run contextual information.
    :param index: Run specific account index. 

    :returns: A cached account.

    """
    return get_account(factory.create_account_id(
        index,
        ctx.network,
        ctx.run,
        ctx.run_type
        ))


def get_run_network(ctx: RunContext) -> Network:
    """Decaches domain object: Network.
    
    :param ctx: Generator run contextual information.

    :returns: A registered network.

    """
    network_id = factory.create_network_id(ctx.network)

    return get_network(network_id)


def get_run_node(ctx: RunContext) -> Node:
    """Decaches domain object: Node.
    
    :param ctx: Generator run contextual information.

    :returns: A registered node.

    """
    # Pull healthy nodes.
    network_id = factory.create_network_id(ctx.network)
    nodes = [i for i in get_nodes(network_id) if i.status == NodeStatus.HEALTHY] 
    if not nodes:
        raise ValueError(f"Network {network_id.name} has no registered healthy nodes.")
    
    # Select random if node index unspecified.
    if ctx.node <= 0 or ctx.node is None:
        return random.choice(nodes)

    # Select specific with fallback to random.
    try:
        return nodes[ctx.node - 1]
    except IndexError:
        return random.choice(nodes)