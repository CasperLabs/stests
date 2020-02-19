import random
import typing

from stests.core.cache.utils import decache
from stests.core.cache.identifiers import AccountIdentifier
from stests.core.cache.identifiers import NetworkIdentifier
from stests.core.cache.identifiers import NodeIdentifier
from stests.core.domain import Account
from stests.core.domain import Network
from stests.core.domain import Node



@decache
def get_account(account_id: AccountIdentifier) -> Account:
    """Decaches domain object: Account.
    
    """
    run = account_id.run

    return [
        "run-account",
        run.network.name,
        run.type,
        f"R-{str(run.index).zfill(3)}",
        f"{str(account_id.index).zfill(6)}"
    ]


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
