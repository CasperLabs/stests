import typing

from stests.core import cache
from stests.core import factory
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.types.orchestration import ExecutionContext



def get_network_node(ctx: ExecutionContext) -> typing.Tuple[Network, Node]:
    """Returns the network and node to which deploy(s) will be dispatched.

    :param ctx: Execution context information.

    :returns: 2 member tuple -> (network, node).
    
    """
    network_id = factory.create_network_id(ctx.network)
    network = cache.infra.get_network(network_id)
    node = cache.infra.get_node_by_network(network)

    return network, node
