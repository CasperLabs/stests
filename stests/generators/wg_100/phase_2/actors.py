from stests.core import cache
from stests.core import clx
from stests.core.domain import RunContext
from stests.core.mq.actor import actorify
from stests.core.utils import resources
from stests.generators.wg_100 import constants



@actorify()
def do_deploy_contract(ctx: RunContext):
    """Deploys smart contract to target network.
    
    :param ctx: Generator run contextual information.

    """
    binary_fpath = resources.get_wasm_path(constants.WASM_CONTRACT_FILENAME)
    print("TODO: phase_2")


@actorify()
def do_start_auction(ctx):
    """Initialise auction phase.
    
    :param ctx: Generator run contextual information.

    """
    print("TODO: do_start_auction :: 1. Establish transfer sequence.")

    # Chain.
    return ctx
