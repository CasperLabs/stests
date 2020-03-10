import argparse

from stests.core import cache
from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger

from stests.core.orchestration import ExecutionAspect
from stests.core.orchestration import ExecutionInfo

from stests.generators.wg_100 import args



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays informations regarding a generators run.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )

# CLI argument: run type.
ARGS.add_argument(
    "--run-type",
    help=f"Generator type - e.g. wg-100.",
    dest="run_type",
    type=args_validator.validate_run_type,
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Unpack.
    network_id = factory.create_network_id(args.network)

    # Pull execution information.
    info_list = cache.orchestration.get_info_list(network_id, args.run_type)
    info_list = [i for i in info_list if i.aspect == ExecutionAspect.RUN]
    if not info_list:
        logger.log("No run information found.")
        return    

    # Display header.
    print("-----------------------------------------------------------------------------------------------")
    print(f"Network    :: Type   :: ID    :: {'Started'.ljust(26)} :: {'Time (secs)'.rjust(11)} :: Status")
    print("-----------------------------------------------------------------------------------------------")

    # Display details.
    for info in sorted(info_list, key=lambda i: i.run_index):
        if info.aspect == ExecutionAspect.RUN:
            print(f"{network_id.name.ljust(10)} :: {info.run_type} :: {info.index_label.strip()} :: {info.ts_start} :: {info.tp_elapsed_label.rjust(11)} :: {info.status_label}")


    # Display footer.
    print("-----------------------------------------------------------------------------------------------")
    print(f"total runs = {len(info_list)}")
    print("-----------------------------------------------------------------------------------------------")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
