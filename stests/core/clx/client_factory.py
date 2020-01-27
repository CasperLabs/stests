import casperlabs_client
from stests.core.utils.workflow import WorkflowContext



def get_client(ctx: WorkflowContext) -> casperlabs_client.CasperLabsClient:
    """Factory method to return configured clabs client.
    
    """
    # TODO: get node id / client ssl cert from ctx.
    return casperlabs_client.CasperLabsClient()
