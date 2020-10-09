import argparse

from stests.core import cache
from stests.core import factory
from stests.core.types.infra import NetworkStatus
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env



# CLI argument parser.
ARGS = argparse.ArgumentParser("Updates network status within stests cache.")

# CLI argument: network name.
ARGS.add_argument(
    "--net",
    default=env.get_network_name(),
    dest="network",
    help="Network name {type}{id}, e.g. nctl1.",
    type=args_validator.validate_network,
    )

# Set CLI argument: network status.
ARGS.add_argument(
    "--status",
    choices=[i.name.lower() for i in NetworkStatus],
    dest="status",
    help="Network status.",
    type=str
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Pull.
    network_id = factory.create_network_id(args.network)
    network = cache.infra.get_network(network_id)
    if network is None:
        raise ValueError("Unregistered network.")

    # Update.
    network.status = NetworkStatus[args.status.upper()]

    # Push.
    cache.infra.set_network(network)

    # Notify.
    utils.log(f"Network {args.network} status was updated --> {network.status}")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
