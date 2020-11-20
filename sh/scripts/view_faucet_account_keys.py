import argparse

from stests.core import cache
from stests.core import factory
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env
from arg_utils import get_network



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays a keys asssociated with a network's faucet account.")

# CLI argument: network name.
ARGS.add_argument(
    "--net",
    default=env.get_network_name(),
    dest="network",
    help="Network name {type}{id}, e.g. nctl1.",
    type=args_validator.validate_network,
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    network = get_network(args)
    utils.log(f"NETWORK: {network.name} -> faucet account-key = {network.faucet.account_key}")
    utils.log(f"NETWORK: {network.name} -> faucet account-hash = {network.faucet.account_hash}")
    utils.log(f"NETWORK: {network.name} -> faucet private-key = {network.faucet.private_key}")
    utils.log(f"NETWORK: {network.name} -> faucet public-key = {network.faucet.public_key}")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
