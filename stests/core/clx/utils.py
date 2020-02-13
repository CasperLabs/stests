import casperlabs_client as pyclx

from stests.core import cache
from stests.core.domain import Node
from stests.core.domain import RunContext



def get_client(node: Node) -> pyclx.CasperLabsClient:
    """Factory method to return configured clabs client.
    
    """
    # TODO: get node id / client ssl cert from ctx.
    return pyclx.CasperLabsClient(
        host=node.host,
        port=node.port,
    )


def get_client_from_ctx(ctx: RunContext) -> pyclx.CasperLabsClient:
    """Factory method to return configured clabs client.
    
    """
    # Set node.
    node = cache.get_node_by_ctx(ctx)
    if not node:
        raise ValueError("Network nodeset is empty, therefore cannot dispatch a deploy.")

    return get_client(node)
