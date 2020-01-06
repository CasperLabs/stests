import argparse
import os

from stests.core.mq import init as init_mq_broker
from stests.core.types.core import ExecutionContext
from stests.generators.wg_100 import metadata
from stests.utils import env



# Set command line arguments.
ARGS = argparse.ArgumentParser(f"Executes the {metadata.DESCRIPTION} workload generator.")
ARGS.add_argument(
    "--simulator-run-id",
    help="Simulator run identifier.",
    dest="simulator_run_id",
    type=int,
    default=0
    )
ARGS.add_argument(
    "--network-id",
    help="Network identifier.",
    dest="network_id",
    type=str,
    default=env.get_network_id()
    )


def main():
    """Worker entry point.
    
    """
    # Initialise execution context.
    ctx = ExecutionContext(ARGS.network_id, metadata.ID, ARGS.simulator_run_id)

    # Initialise mq broker.
    init_mq_broker(ctx.network_id)

    # Import actors of relevance.
    # Note: currently we must import actors AFTER the mq broker is initiialised.
    from stests.generators.wg_100.phase_01.actors import contract
    from stests.generators.wg_100.phase_01.actors import user



if __name__ == "__main__":
    ARGS, _ = ARGS.parse_known_args()
    main()