import casperlabs_client as pyclx
from stests.core.domain import Node



def get_client(node: Node) -> pyclx.CasperLabsClient:
    """Factory method to return configured clabs client.
    
    """
    # TODO: get node id / client ssl cert from ctx.
    return pyclx.CasperLabsClient(
        host=node.host,
        port=node.port,
    )
