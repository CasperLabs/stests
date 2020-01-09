import argparse
import os

from stests.core.utils import env
from stests.core.utils.execution import ExecutionContext
from stests.core.utils.execution import init_services
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


def main(args):
    """Worker entry point.
    
    """
    # Set context.
    ctx = ExecutionContext.create(args.network_id, metadata.ID)

    # Initialise execution services.
    init_services(ctx)

    # Import actors of relevance.
    # Note: currently we must import actors AFTER servcies are initiialised.
    from stests.generators.wg_100.phase_01.actors import contract
    from stests.generators.wg_100.phase_01.actors import user


# Auto-invoke.
main(ARGS.parse_known_args()[0])
