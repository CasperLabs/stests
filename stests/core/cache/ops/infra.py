import random
import typing

from stests.core import factory
from stests.core.cache.model import Item
from stests.core.cache.model import ItemKey
from stests.core.cache.model import SearchKey
from stests.core.cache.model import StoreOperation
from stests.core.cache.model import StorePartition
from stests.core.cache.ops.utils import cache_op
from stests.core.types.chain import ContractType
from stests.core.types.chain import NamedKey
from stests.core.types.infra import Network
from stests.core.types.infra import NetworkIdentifier
from stests.core.types.infra import Node
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext



# Cache partition.
_PARTITION = StorePartition.INFRA

# Cache collections.
COL_NAMED_KEY = "named-key"
COL_NETWORK = "network"
COL_NODE = "node"


@cache_op(_PARTITION, StoreOperation.GET_ONE_FROM_MANY)
def get_named_key(network: str, contract_type: ContractType, name: str) -> ItemKey:
    """Decaches domain objects: NamedKey.

    :param network: A pointer to either a network or network identifier.

    :returns: Collection of registered nodes.

    """
    return ItemKey(
        paths=[
            network,
            COL_NAMED_KEY,
            "A-*",
            contract_type.name,
        ],
        names=[
            name,
        ]
    )


@cache_op(_PARTITION, StoreOperation.GET_MANY)
def get_named_keys(network: typing.Union[NetworkIdentifier, Network, str]) -> SearchKey:
    """Decaches domain objects: NamedKey.

    :param network: A pointer to either a network or network identifier.

    :returns: Collection of registered nodes.

    """
    try:
        network = network.name
    except AttributeError:
        pass

    return SearchKey(
        paths=[
            network,
            COL_NAMED_KEY,
        ]
    )


@cache_op(_PARTITION, StoreOperation.GET_ONE)
def get_network(network_id: NetworkIdentifier) -> ItemKey:
    """Decaches domain object: Network.

    :param network_id: A network identifier.

    :returns: A registered network.

    """
    return ItemKey(
        paths=[
            network_id.name,
        ],
        names=[
            COL_NETWORK,
        ]
    )


@cache_op(_PARTITION, StoreOperation.GET_MANY)
def get_networks() -> SearchKey:
    """Decaches domain objects: Network.

    :returns: List of registered networks.

    """
    return SearchKey(
        paths=[
            "*",
            COL_NETWORK,
        ]
    )


@cache_op(_PARTITION, StoreOperation.GET_ONE)
def get_node(node_id: NodeIdentifier) -> ItemKey:
    """Decaches domain object: Node.

    :param node_id: A node identifier.

    :returns: A registered node.

    """
    return ItemKey(
        paths=[
            node_id.network.name,
            COL_NODE,
        ],
        names=[
            node_id.label_index,
        ]
    )


def get_node_by_network(network: typing.Union[Network, NetworkIdentifier]) -> Node:
    """Decaches domain object: Node.

    :param network: A network.

    :returns: A registered node selected at random from a network's nodeset.

    """
    nodeset = get_nodes_for_dispatch(network)
    if not nodeset:
        raise ValueError(f"Network {network.name} has no registered operational nodes.")

    return random.choice(nodeset)


def get_node_by_account_key(network: typing.Union[Network, NetworkIdentifier], account_key: str) -> Node:
    """Decaches domain object: Node.

    :param network: A network.
    :param account_key: Key of account associated with a validator.

    :returns: A registered node.

    """
    nodeset = get_nodes_for_dispatch(network)
    if not nodeset:
        raise ValueError(f"Network {network.name} has no registered operational nodes.")

    for node in nodeset:
        if node.account.account_key == account_key:
            return node


@cache_op(_PARTITION, StoreOperation.GET_MANY)
def get_nodes(network: typing.Union[NetworkIdentifier, Network]=None) -> SearchKey:
    """Decaches domain objects: Node.

    :param network: A pointer to either a network or network identifier.

    :returns: Collection of registered nodes.

    """
    return SearchKey(
        paths=[
            "*" if network is None else network.name,
            COL_NODE,
        ]
    )


def get_nodes_for_dispatch(network: typing.Union[NetworkIdentifier, Network], sample_size: int = None) -> typing.List[Node]:
    """Decaches domain objects: Node (if dispatcheable).

    :param network: A pointer to either a network or network identifier.

    :returns: Collection of registered nodes.

    """
    return _get_nodes(network, sample_size, lambda i: i.is_dispatchable)


def get_nodes_for_monitoring(network: typing.Union[NetworkIdentifier, Network], sample_size: int = None) -> typing.List[Node]:
    """Decaches domain objects: Node (if monitorable).

    :param network: A pointer to either a network or network identifier.

    :returns: Collection of registered nodes.

    """
    return _get_nodes(network, sample_size, lambda i: i.is_monitorable)


def get_nodes_for_query(network: typing.Union[NetworkIdentifier, Network], sample_size: int = None) -> typing.List[Node]:
    """Decaches domain objects: Node (if queryable).

    :param network: A pointer to either a network or network identifier.

    :returns: Collection of registered nodes.

    """
    return _get_nodes(network, sample_size, lambda i: i.is_queryable)


def _get_nodes(
    network: typing.Union[NetworkIdentifier, Network],
    sample_size: typing.Optional[int],
    predicate: typing.Callable,
    ) -> typing.List[Node]:
    """Decaches domain objects: Node.

    """
    nodeset = [i for i in get_nodes(network) if predicate(i)]
    if sample_size is not None:
        sample_size = min(sample_size, len(nodeset))

    return nodeset if sample_size is None else random.sample(nodeset, sample_size)


@cache_op(_PARTITION, StoreOperation.SET_ONE)
def set_named_key(named_key: NamedKey) -> Item:
    """Encaches domain object: NamedKey.

    :param network: NamedKey domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return Item(
        item_key=ItemKey(
            paths=[
                named_key.network,
                COL_NAMED_KEY,
                named_key.label_account_index,
                named_key.contract_type.name,
            ],
            names=[
                named_key.name
            ]
        ),
        data=named_key
    )


@cache_op(_PARTITION, StoreOperation.SET_ONE)
def set_network(network: Network) -> Item:
    """Encaches domain object: Network.

    :param network: Network domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return Item(
        item_key=ItemKey(
            paths=[
                network.name,
            ],
            names=[
                COL_NETWORK,
            ]
        ),
        data=network,
    )


@cache_op(_PARTITION, StoreOperation.SET_ONE)
def set_node(node: Node) -> Item:
    """Encaches domain object: Node.

    :param node: Node domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return Item(
        item_key=ItemKey(
            paths=[
                node.network,
                COL_NODE,
            ],
            names=[
                node.label_index,
            ]
        ),
        data=node,
    )
