import argparse

from stests.core import cache
from stests.core import clx
from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger


# CLI argument parser.
ARGS = argparse.ArgumentParser("Lists a network's faucet balance.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )

# CLI argument: network name.
ARGS.add_argument(
    "address",
    help="Network address (hex format), e.g. 853b4f5e2cb1e05416dc8af8ebdfae792b5c7b9246172450c0df9bff88c28297.",
    type=str
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    network_id=factory.create_network_id(args.network)

    balance = clx.get_account_balance_by_address(network_id, args.address)

    logger.log(f"""NETWORK: {network_id.name} -> account balance = {balance}""")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
