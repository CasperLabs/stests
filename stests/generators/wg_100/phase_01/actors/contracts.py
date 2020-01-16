import dramatiq

from stests.core.cache import accessor as cache
from stests.core.types import AccountType
from stests.generators.wg_100 import metadata


# Queue to which message will be dispatched.
_QUEUE = f"{metadata.ID}.phase_01.contract"


@dramatiq.actor(queue_name=_QUEUE)
def deploy_contract(ctx, account):
    """Deploys smart contract to target network.
    
    """
    # Pull wasm.
    print("TODO: pull wasm blob and deploy")
