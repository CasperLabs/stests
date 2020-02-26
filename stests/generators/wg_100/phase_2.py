import time
import typing

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.domain import Account
from stests.core.domain import AccountType
from stests.core.domain import NetworkIdentifier
from stests.core.domain import Node
from stests.core.domain import NodeIdentifier
from stests.core.domain import RunContext
from stests.core.mq.actor import actorify
from stests.core.utils import factory
from stests.core.utils import resources
from stests.generators.wg_100 import constants



@actorify(on_success=lambda: do_start_auction)
def do_deploy_contract(ctx: RunContext):
    """Deploys smart contract to target network.
    
    :param ctx: Generator run contextual information.

    """
    print("TODO: do_deploy_contract :: 1. pull account.  2. Dispatch deploy.  3. Monitor deploy.")
    binary_fpath = resources.get_wasm_path(constants.WASM_CONTRACT_FILENAME)
    print(binary_fpath)


@actorify()
def do_start_auction(ctx):
    """Initialise auction phase.
    
    :param ctx: Generator run contextual information.

    """
    print("TODO: do_start_auction :: 1. Establish transfer sequence.")

    # Chain.
    return ctx
