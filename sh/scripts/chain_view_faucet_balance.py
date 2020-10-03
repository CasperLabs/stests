import argparse

from stests.core import cache
from stests.core import clx
from stests.core import factory
from stests.core.utils import args_validator
from stests.core.utils import cli as utils



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays a network's faucet balance.")

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
    network_id=factory.create_network_id(args.network)
    network = cache.infra.get_network(network_id)
    if network is None:
        utils.log_warning(f"Network {args.network} is unregistered.")
        return

    balance = clx.get_account_balance(network_id, network.faucet.account_id)

    utils.log(f"NETWORK: {network.name} -> faucet balance = {balance}")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
