import argparse

from stests.core import cache
from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger

from stests.core.orchestration import ExecutionAspect
from stests.core.orchestration import ExecutionInfo

from stests.generators.wg_100 import args



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays summary information for a run.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )

# CLI argument: run type.
ARGS.add_argument(
    "run_type",
    help="Generator type - e.g. wg-100.",
    type=args_validator.validate_run_type,
    )

# CLI argument: run index.
ARGS.add_argument(
    "run_index",
    help="Run identifier, e.g. 1-100.",
    type=args_validator.validate_run_index,
    )



def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Unpack.
    network_id = factory.create_network_id(args.network)

    # Pull execution information.
    info_list = cache.orchestration.get_info_list(network_id, args.run_type, args.run_index)
    if not info_list:
        logger.log("No run information found.")
        return

    # Header.
    print("-----------------------------------------------------------------------------------------------")
    print(f"{network_id.name} - {args.run_type}")
    print("-----------------------------------------------------------------------------------------------")

    # Details.
    print(f"Phase / Step       {'Started'.ljust(26)}    {'Time (secs)'.rjust(11)}  Status       Action")
    for info in sorted(info_list, key=lambda i: i.index_label):
        if info.aspect in (ExecutionAspect.RUN, ExecutionAspect.PHASE):
            print("")
        print(f"{info.index_label}    {info.ts_start}    {info.tp_elapsed_label.rjust(11)}  {info.status_label}   {info.step_label if info.step_label else ''}")

    # Footer.
    print("-----------------------------------------------------------------------------------------------")



# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
