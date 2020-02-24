import time
import typing

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.actors.account import do_create_account
from stests.core.actors.account import do_fund_account
from stests.core.domain import Account
from stests.core.domain import AccountType
from stests.core.domain import NetworkIdentifier
from stests.core.domain import Node
from stests.core.domain import NodeIdentifier
from stests.core.domain import RunContext
from stests.core.utils import factory
from stests.core.utils import resources
from stests.generators.wg_100 import constants



# Queue to which message will be dispatched.
_QUEUE = f"generators.{constants.TYPE.lower()}"


@dramatiq.actor(queue_name=_QUEUE)
def do_start_auction(ctx):
    """Initialise auction phase.
    
    :param ctx: Generator run contextual information.

    """
    print("TODO: do_start_auction :: 1. Establish transfer sequence.")

    # Chain.
    return ctx
