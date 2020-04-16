import typing

from casperlabs_client import CasperLabsClient

from stests.core import cache
from stests.core.domain import Network
from stests.core.domain import NetworkIdentifier
from stests.core.domain import Node
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.core.utils import logger



def get_client(src: typing.Union[CasperLabsClient, ExecutionContext, Network, NetworkIdentifier, Node, NodeIdentifier]) -> typing.Tuple[Node, CasperLabsClient]:
    """Factory method to return a configured client plus the node with which it is associated.

    :param src: The source from which a network node will be derived.

    :returns: A 2 member tuple: (Node, configured clabs client).
    
    """
    # In some cases calling code already has a client instance, but as
    # method overloading is unsupported in python, code is simplified with a pass through.  
    if isinstance(src, CasperLabsClient):
        return src.node, src

    # Set node. 
    if isinstance(src, Node):
        node = src
    elif isinstance(src, NodeIdentifier):
        node = cache.infra.get_node(src)
    elif isinstance(src, (Network, NetworkIdentifier)):
        node = cache.infra.get_node_by_network(src)
    elif isinstance(src, ExecutionContext):
        node = cache.infra.get_node_by_ctx(src)
    else:
        raise ValueError("Cannot derive node from input source.")

    if not node:
        raise ValueError("Network nodeset is empty, therefore cannot dispatch a deploy.")

    # TODO: get node id / client ssl cert ?
    client = CasperLabsClient(
        host=node.host,
        port=node.port,
    )
    client.node = node

    return node, client
