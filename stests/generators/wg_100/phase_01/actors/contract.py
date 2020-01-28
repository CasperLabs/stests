import dramatiq

from stests.core import clx
from stests.core.utils import resources
from stests.generators.wg_100 import metadata


# Queue to which message will be dispatched.
_QUEUE = f"{metadata.TYPE}.phase_01.contract"


@dramatiq.actor(queue_name=_QUEUE, actor_name="deploy_contract")
def deploy(ctx, account):
    """Deploys smart contract to target network.
    
    """
    fpath = resources.get_wasm_path(ctx.wasm_contract_filename)
    clx.do_deploy_contract(ctx, account, fpath)
