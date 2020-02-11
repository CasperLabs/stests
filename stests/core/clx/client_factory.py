import casperlabs_client
from stests.core.domain import Node



def get_client(node: Node) -> casperlabs_client.CasperLabsClient:
    """Factory method to return configured clabs client.
    
    """
    # TODO: get node id / client ssl cert from ctx.
    return casperlabs_client.CasperLabsClient(
        host=node.host,
        port=node.port,
    )
