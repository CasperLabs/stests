import dramatiq

from stests.core import clx
from stests.core.utils import resources
from stests.generators.wg_100 import metadata


# Queue to which message will be dispatched.
_QUEUE = f"{metadata.TYPE}.phase_01.contract"

# Name of wasm file - should be compiled into resources/wasm folder.
WASM_CONTRACT_FILENAME="erc20_smart_contract.wasm"


@dramatiq.actor(queue_name=_QUEUE)
def do_deploy_contract(ctx):
    """Deploys smart contract to target network.
    
    """
    print("TODO: do_deploy_contract :: 1. pull account.  2. Dispatch deploy.  3. Monitor deploy.")
    binary_fpath = resources.get_wasm_path(WASM_CONTRACT_FILENAME)
    print(binary_fpath)
    return ctx

    # clx.do_deploy_contract(ctx, account, binary_fpath)
