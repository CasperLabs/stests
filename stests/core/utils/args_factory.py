import argparse

from stests.core.utils import args_validator
from stests.core.orchestration import ExecutionMode



def get_argparser_for_generator(description: str) -> argparse.ArgumentParser:
    """Factory method: returns standard argument parser for a generator.
    
    :param description: Description ofto be assigned to parser.

    :returns: Standard argument parser for a generator.

    """
    # Set command line arguments.
    args = argparse.ArgumentParser(f"Executes {description} workflow.")

    # network name.
    args.add_argument(
        "network_name",
        help="Network name {type}{id}, e.g. lrt1.",
        type=args_validator.validate_network,
        )

    # deploys per second.
    args.add_argument(
        "--deploys-per-second",
        dest="deploys_per_second",
        help="Number of deploys to dispatch per second.",
        type=args_validator.validate_deploys_per_second,
        default=0,
        )

    # execution mode.
    args.add_argument(
        "--execution-mode",
        dest="execution_mode",
        help="Generator execution mode - sequential | periodical.",
        type=args_validator.validate_execution_mode,
        default=ExecutionMode.SEQUENTIAL.name.lower(),
        )

    # node index.
    args.add_argument(
        "--node",
        dest="node_index",
        help="Node index - must be between 1 and 999. If specified deploys are dispatched to this node only, otherwise deploys are dispatched to random nodes.",
        type=args_validator.validate_node_index,
        default=0,
        required=False,
        )

    # run index.
    args.add_argument(
        "--run",
        dest="run_index",
        help="Generator run index - must be between 1 and 65536.",
        type=args_validator.validate_run_index,
        default=1,
        )

    # loop interval.
    args.add_argument(
        "--loop-interval",
        dest="loop_interval",
        help="Interval in seconds between loops.",
        type=args_validator.validate_loop_interval,
        default=0,
        )

    # loop count.
    args.add_argument(
        "--loop-count",
        dest="loop_count",
        help="Number of times to loop.",
        type=args_validator.validate_loop_count,
        default=0,
        )
    
    return args
