import time

import casperlabs_client as pyclx
import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.types import Account
from stests.core.types import AccountType
from stests.generators.wg_100 import metadata


# Queue to which message will be dispatched.
_QUEUE = f"{metadata.TYPE}.phase_01.auction"


@dramatiq.actor(queue_name=_QUEUE)
def do_start_auction(ctx):
    print("TODO: do_start_auction :: 1. Establish transfer sequence.")

    return ctx