from stests.core import cache
from stests.core import clx
from stests.core.orchestration import ExecutionRunInfo
from stests.core.mq.actor import actorify
from stests.core.utils import resources
from stests.generators.wg_100 import constants

from stests.generators.wg_100.phase_3 import do_refund_step_1


@actorify(on_success=lambda: do_start_auction)
def do_deploy_contract(ctx: ExecutionRunInfo):
    """Deploys smart contract to target network.
    
    :param ctx: Generator run contextual information.

    """
    binary_fpath = resources.get_wasm_path(constants.WASM_CONTRACT_FILENAME)
    print("TODO: deploy erc-20 contract")


@actorify(on_success=lambda: do_refund_step_1)
def do_start_auction(ctx):
    """Initialise auction phase.
    
    :param ctx: Generator run contextual information.

    """
    print("TODO: start auction")
