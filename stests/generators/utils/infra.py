import typing

from stests.core import cache
from stests.core import factory
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext



def get_network_node(src: typing.Union[ExecutionContext, NodeIdentifier], node_index=None) -> typing.Tuple[Network, Node]:
    """Returns the network and node to which deploy(s) will be dispatched.

    :param src: Source from which targets will be derived.

    :returns: 2 member tuple -> (network, node).
    
    """
    if isinstance(src, ExecutionContext):
        network_id = factory.create_network_id(src.network)
        network = cache.infra.get_network(network_id)
        if node_index is not None:
            node_id = factory.create_node_id(network_id, node_index)
            node = cache.infra.get_node(node_id)
        elif src.node_index != 0:
            node_id = factory.create_node_id(network_id, src.node_index)
            node = cache.infra.get_node(node_id)
        else:
            node = cache.infra.get_node_by_network(network)

    elif isinstance(src, NodeIdentifier):
        network = cache.infra.get_network(src.network_id)
        node = cache.infra.get_node(src)

    else:
        raise ValueError("Cannot derive network & node from source")

    return network, node
