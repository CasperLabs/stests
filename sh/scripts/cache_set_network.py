import argparse

from stests.core import cache
from stests.core import factory
from stests.core.utils import args_validator
from stests.core.utils import cli as utils



# CLI argument parser.
ARGS = argparse.ArgumentParser("Upload network information to stests.")

# CLI argument: network name.
ARGS.add_argument(
    "--net",
    default="nctl1",
    dest="network",
    help="Network name {type}{id}, e.g. nctl1.",
    type=args_validator.validate_network,
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Instantiate.
    network = factory.create_network(args.network)

    # Push.
    cache.infra.set_network(network)

    # Inform.
    utils.log(f"Network {args.network} was successfully registered")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())