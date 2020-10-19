import argparse

from stests.core import cache
from stests.core import factory
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env


# CLI argument parser.
ARGS = argparse.ArgumentParser("Upload network information to stests.")

# CLI argument: network name.
ARGS.add_argument(
    "--net",
    default=env.get_network_name(),
    dest="network",
    help="Network name {type}{id}, e.g. nctl1.",
    type=args_validator.validate_network,
    )

# CLI argument: network name.
ARGS.add_argument(
    "--chain",
    default="casperlabs-example",
    dest="chain",
    help="Chain name, e.g. cspr-001.",
    type=str,
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Instantiate.
    network = factory.create_network(args.network, args.chain)

    # Push.
    cache.infra.set_network(network)

    # Inform.
    utils.log(f"Network {args.network} was successfully registered")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
