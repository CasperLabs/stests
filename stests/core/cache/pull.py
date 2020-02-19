import random
import typing

from stests.core.cache.utils import decache1
from stests.core.cache.identifiers import AccountIdentifier
from stests.core.cache.identifiers import NetworkIdentifier
from stests.core.cache.identifiers import NodeIdentifier
from stests.core.domain import Account
from stests.core.domain import Network
from stests.core.domain import Node



@decache1
def get_account(account_id: AccountIdentifier) -> Account:
    """Decaches domain object: Account.
    
    """
    run = account_id.run

    return [
        "account",
        run.network.name,
        run.type,
        f"R-{str(run.index).zfill(3)}",
        f"{str(account_id.index).zfill(6)}"
    ]


@decache1
def get_network(network_id: NetworkIdentifier) -> Network:
    """Decaches domain object: Network.
    
    """
    return [
        "network",
        network_id.name
    ]


@decache1
def get_networks() -> typing.List[Network]:
    """Decaches domain objects: Network.
    
    """
    return ["network", "*"]


@decache1
def get_node(node_id: NodeIdentifier) -> Node:
    """Decaches domain object: Node.
    
    """
    return [
        "node",
        node_id.network.name,
        f"N-{str(node_id.index).zfill(4)}"
    ]


@decache1
def get_nodes(network_id: NetworkIdentifier=None) -> typing.List[Node]:
    """Decaches domain objects: Node.
    
    """
    if network_id is None:
        return ["node", "*"]
    else:
        return [
            "node",
            network_id.name,
            "N-*"
        ]
