import argparse

from stests.core import cache
from stests.core.utils import args_validator
from stests.core.utils import factory
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
    # Instantiate.
    network = factory.create_network(args.network)

    # Push.
    cache.set_network(network)

    print(cache.get_networks())

    # Inform.
    logger.log(f"Network {args.network} was successfully registered")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
