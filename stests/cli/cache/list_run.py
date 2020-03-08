import argparse

from stests.core import cache
from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger
from stests.core.utils import encoder


from stests.generators.wg_100 import args



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays informations regarding a generators run.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )

# CLI argument: generator.
ARGS.add_argument(
    "run_type",
    help="Generator type - e.g. wg-100.",
    type=args_validator.validate_run_type
    )

# CLI argument: run index.
ARGS.add_argument(
    "run_index",
    help="Generator run index - must be between 1 and 65536.",
    type=args_validator.validate_run_index
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Pull run context.
    network_id = factory.create_network_id(args.network)
    ctx = cache.orchestration.get_context(
        network_id.name, 
        args.run_index,
        args.run_type
        )
    if ctx is None:
        logger.log_warning(f"Run {network_id.name} : {args.run_type} : {args.run_index} is not found.")
        return

    # Pull run steps.
    steps = cache.orchestration.get_steps(ctx)
    if not steps:
        logger.log_warning(f"Run {network_id.name} : {args.run_type} : {str(args.run_index).zfill(4)} is unexecuted.")
        return

    # Display.
    print("-----------------------------------------------------------------------------------------------")
    print(f"Run {ctx.network} : {ctx.run_type} : R-{str(args.run_index).zfill(4)}")
    print("-----------------------------------------------------------------------------------------------")
    for idx, step in enumerate(sorted(steps, key=lambda s: s.ts_start)):
        print(f"step {str(idx + 1).zfill(2)} :: {step.action.ljust(22)} :: {step.status.name.ljust(11)} :: {step.ts_start} :: {step.tp_duration_label.rjust(11)}")
    print("-----------------------------------------------------------------------------------------------")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
