import casperlabs_client
from stests.core.domain import RunContext



def get_client(ctx: RunContext) -> casperlabs_client.CasperLabsClient:
    """Factory method to return configured clabs client.
    
    """
    # TODO: get node id / client ssl cert from ctx.
    return casperlabs_client.CasperLabsClient()
