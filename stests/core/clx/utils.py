import typing

import casperlabs_client as pyclx

from stests.core import cache
from stests.core.domain import NetworkIdentifier
from stests.core.domain import Node
from stests.core.domain import NodeIdentifier
from stests.core.domain import RunContext
from stests.core.utils import logger



def get_client(src: typing.Union[Node, NodeIdentifier, NetworkIdentifier, RunContext]) -> typing.Tuple[Node, pyclx.CasperLabsClient]:
    """Factory method to return a configured clabs client and the node with which it is associated.

    :param src: The source from which a network node will be derived.

    :returns: A configured clabs client ready for use.
    
    """
    # Set node. 
    if isinstance(src, Node):
        node = src
    elif isinstance(src, NodeIdentifier):
        node = cache.get_node(src)
    elif isinstance(src, NetworkIdentifier):
        node = cache.get_node_by_network_id(src)
    elif isinstance(src, RunContext):
        node = cache.get_node_by_run_context(src)

    if not node:
        raise ValueError("Network nodeset is empty, therefore cannot dispatch a deploy.")

    log_info(f"connecting to node :: {node.network}:N-{str(node.index).zfill(4)} :: {node.host}:{node.port}")

    # TODO: get node id / client ssl cert.
    return node, pyclx.CasperLabsClient(
        host=node.host,
        port=node.port,
    )


def log_info(msg):
    """Helper logging function.
    
    """
    logger.log(f"PYCLX :: {msg}")
