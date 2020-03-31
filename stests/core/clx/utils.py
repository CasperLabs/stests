import typing

import casperlabs_client

from stests.core import cache
from stests.core.domain import Network
from stests.core.domain import NetworkIdentifier
from stests.core.domain import Node
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.core.utils import logger



def get_client(src: typing.Union[ExecutionContext, Network, NetworkIdentifier, Node, NodeIdentifier]) -> typing.Tuple[Node, casperlabs_client.CasperLabsClient]:
    """Factory method to return a configured clabs client and the node with which it is associated.

    :param src: The source from which a network node will be derived.

    :returns: A configured clabs client ready for use.
    
    """
    # Set node. 
    if isinstance(src, Node):
        node = src
    elif isinstance(src, NodeIdentifier):
        node = cache.infra.get_node(src)
    elif isinstance(src, Network):
        node = cache.infra.get_node_by_network_id(src)
    elif isinstance(src, NetworkIdentifier):
        node = cache.infra.get_node_by_network_id(src)
    elif isinstance(src, ExecutionContext):
        node = cache.infra.get_node_by_ctx(src)
    else:
        raise ValueError("Cannot derive node from input source.")

    if not node:
        raise ValueError("Network nodeset is empty, therefore cannot dispatch a deploy.")

    # TODO: get node id / client ssl cert.
    return node, casperlabs_client.CasperLabsClient(
        host=node.host,
        port=node.port,
    )
