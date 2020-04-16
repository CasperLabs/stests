import argparse

from stests.core import cache
from stests.core.types.infra import NetworkStatus
from stests.core.utils import args_validator
from stests.core import factory
from stests.core.utils import logger


# CLI argument parser.
ARGS = argparse.ArgumentParser("Informs stests of a mutation in the status of a network.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )

# Set CLI argument: network status.
ARGS.add_argument(
    "status",
    choices=[i.name.lower() for i in NetworkStatus],
    help="Network status.",
    type=str
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Pull.
    network = cache.infra.get_network_by_name(args.network)
    if network is None:
        raise ValueError("Unregistered network.")

    # Update.
    network.status = NetworkStatus[args.status.upper()]

    # Push.
    cache.infra.set_network(network)

    # Notify.
    logger.log(f"Network {args.network} status was updated --> {network.status}")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
