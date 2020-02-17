import typing

import casperlabs_client as pyclx

from stests.core import cache
from stests.core.cache import NetworkIdentifier
from stests.core.domain import Node
from stests.core.domain import RunContext



def get_client(src: typing.Union[Node, RunContext, NetworkIdentifier]) -> pyclx.CasperLabsClient:
    """Factory method to return configured clabs client.
    
    """
    if isinstance(src, Node):
        node = src
    elif isinstance(src, NetworkIdentifier):
        node = cache.get_node_by_network_id(src)
    elif isinstance(src, RunContext):
        node = cache.get_node_by_ctx(src)

    if not node:
        raise ValueError("Network nodeset is empty, therefore cannot dispatch a deploy.")

    # TODO: get node id / client ssl cert.
    return pyclx.CasperLabsClient(
        host=node.host,
        port=node.port,
    )
