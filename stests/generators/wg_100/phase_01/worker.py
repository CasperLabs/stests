import argparse
import os

from stests.core.mq.initialiser import init as init_broker
from stests.core.utils import env
from stests.core.utils.workflow import WorkflowArguments
from stests.core.utils.workflow import WorkflowContext

from stests.generators.wg_100 import metadata
from stests.generators.wg_100.args import Arguments


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
# TODO: tidy.
args_parser = WorkflowArguments.get_parser_for_workflow(metadata.DESCRIPTION)
parsed_args, _ = args_parser.parse_known_args()
args = WorkflowArguments.create(None, metadata.TYPE, parsed_args)

# Set context.
ctx = WorkflowContext.create(args)

# Initialise broker & import actors.
init_broker(ctx)
from stests.generators.wg_100.phase_01.actors import accounts
from stests.generators.wg_100.phase_01.actors import contract
