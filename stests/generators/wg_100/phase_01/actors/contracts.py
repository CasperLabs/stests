import dramatiq

from stests.core import clx
from stests.core.cache import accessor as cache
from stests.core.types import AccountType
from stests.core.utils import resources
from stests.generators.wg_100 import metadata


# Queue to which message will be dispatched.
_QUEUE = f"{metadata.ID}.phase_01.contract"

# Filename of the compiled contract.
_CONTRACT_BINARY_FNAME = "erc20_smart_contract.wasm"


@dramatiq.actor(queue_name=_QUEUE)
def deploy_contract(ctx, account):
    """Deploys smart contract to target network.
    
    """
    fpath = resources.get_wasm_path(_CONTRACT_BINARY_FNAME)

    clx.deploys.dispatch(account, fpath)
