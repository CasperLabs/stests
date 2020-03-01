import argparse

from stests.core import cache
from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger


# CLI argument parser.
ARGS = argparse.ArgumentParser(f"Flushes cache of all network related information.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Set network.
    network_id=factory.create_network_id(args.network)
    network = cache.get_network(network_id)
    if network is None:
        logger.log_warning(f"Network {args.network} is unregistered - flushing cache anyway.")

    # Flush cache.
    cache.flush_by_network(network_id)

    # Inform.
    logger.log(f"Network {args.network} cache data was successfully flushed")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
