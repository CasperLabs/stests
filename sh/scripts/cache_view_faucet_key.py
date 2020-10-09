import argparse

from stests.core import cache
from stests.core import factory
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays a network's faucet asymmetric key pair.")

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
    network_id=factory.create_network_id(args.network)
    network = cache.infra.get_network(network_id)
    if network is None:
        utils.log_warning(f"Network {args.network} is unregistered.")
        return

    utils.log(f"NETWORK: {network.name} -> faucet account-hash = {network.faucet.account_hash}")
    utils.log(f"NETWORK: {network.name} -> faucet account-id = {network.faucet.account_id}")
    utils.log(f"NETWORK: {network.name} -> faucet private-key = {network.faucet.private_key}")
    utils.log(f"NETWORK: {network.name} -> faucet public-key = {network.faucet.public_key}")

# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
