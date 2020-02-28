import typing

import casperlabs_client as pyclx

from stests.core import cache
from stests.core.domain import Node
from stests.core.domain import NetworkIdentifier
from stests.core.domain import RunContext
from stests.core.utils import logger



def get_client(src: typing.Union[Node, RunContext, NetworkIdentifier]) -> pyclx.CasperLabsClient:
    """Factory method to return configured clabs client.

    :param src: The source form which a network node will be derived.

    :returns: A configured clabs client ready for use.
    
    """
    _, client = get_client_and_node(src)

    return client


def get_client_and_node(src: typing.Union[Node, RunContext, NetworkIdentifier]) -> pyclx.CasperLabsClient:
    """Factory method to return a configured clabs client and the node with which it is associated.

    :param src: The source form which a network node will be derived.

    :returns: A configured clabs client ready for use.
    
    """
    # Pull node information from cache. 
    if isinstance(src, Node):
        node = src
    elif isinstance(src, NetworkIdentifier):
        node = cache.get_node_by_network_id(src)
    elif isinstance(src, RunContext):
        node = cache.get_run_node(src)

    if not node:
        raise ValueError("Network nodeset is empty, therefore cannot dispatch a deploy.")

    logger.log(f"PYCLX :: connecting to node :: {node.network}:N-{str(node.index).zfill(4)} :: {node.host}:{node.port}")

    # TODO: get node id / client ssl cert.
    return node, pyclx.CasperLabsClient(
        host=node.host,
        port=node.port,
    )