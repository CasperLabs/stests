import dramatiq

from stests.core import clx
from stests.core.utils import resources
from stests.generators.wg_100 import metadata


# Queue to which message will be dispatched.
_QUEUE = f"{metadata.TYPE}.phase_01.contract"

# Name of wasm file - should be compiled into resources/wasm folder.
WASM_CONTRACT_FILENAME="erc20_smart_contract.wasm"


@dramatiq.actor(queue_name=_QUEUE, actor_name="deploy_contract")
def deploy(ctx, account):
    """Deploys smart contract to target network.
    
    """
    binary_fpath = resources.get_wasm_path(WASM_CONTRACT_FILENAME)
    clx.do_deploy_contract(ctx, account, binary_fpath)
