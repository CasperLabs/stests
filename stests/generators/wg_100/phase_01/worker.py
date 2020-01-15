import argparse
import os

from stests.core.mq.initialiser import init as init_broker
from stests.core.utils import env
from stests.core.utils.execution import ExecutionContext
from stests.generators.wg_100 import metadata



# Set command line arguments.
ARGS = argparse.ArgumentParser(f"Executes the {metadata.DESCRIPTION} workload generator.")
ARGS.add_argument(
    "--network-id",
    help="Network identifier.",
    dest="network_id",
    type=str,
    default=env.get_network_id()
    )


# Set args filtering out dramatiq specific.
args, _ = ARGS.parse_known_args()

# Set context.
ctx = ExecutionContext.create(args.network_id, metadata.ID)

# Initialise broker.
init_broker(ctx)

# Import actors of relevance (AFTER broker is initialised).
from stests.generators.wg_100.phase_01.actors import accounts
from stests.generators.wg_100.phase_01.actors import contracts
