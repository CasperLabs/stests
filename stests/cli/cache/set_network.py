import argparse

from stests.core import cache
from stests.core.types import Network
from stests.core.types import NetworkType
from stests.core.utils import args_validator
from stests.core.utils import logger


# CLI argument parser.
ARGS = argparse.ArgumentParser("Upload network information to stests.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network_name
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    instance = Network.create(
        index=int(args.network[3:]),
        typeof=NetworkType[args.network[:3].upper()]
    )
    cache.set_network(instance)
    logger.log("Network information successfully registered")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
