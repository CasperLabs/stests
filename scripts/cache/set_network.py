import argparse

from scripts.cache import utils
from stests.core import cache
from stests.core.types import Network
from stests.core.types import NetworkType
from stests.core.utils import args_validator


# CLI argument parser.
ARGS = argparse.ArgumentParser("Upload network information to stests.")

# CLI argument: network type.
ARGS.add_argument(
    "type",
    choices=[i.name.lower() for i in NetworkType],
    help="Type of network being tested.",
    type=str
    )

# CLI argument: network index.
ARGS.add_argument(
    "idx",
    help="Network index - must be between 1 and 99.",
    type=args_validator.validate_network_idx
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    cache.set_network(Network(
        idx=args.idx,
        typeof=NetworkType[args.type.upper()]
    ))


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
