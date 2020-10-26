import argparse

from stests.core import cache
from stests.core import factory
from stests.core.types.chain import AccountType
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env
from utils import get_network_node



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays a node's bonding asymmetric ECC key pair.")

# CLI argument: network name.
ARGS.add_argument(
    "--net",
    default=env.get_network_name(),
    dest="network",
    help="Network name {type}{id}, e.g. nctl1.",
    type=args_validator.validate_network,
    )

# CLI argument: node index.
ARGS.add_argument(
    "--node",
    default=1,
    dest="node",
    help="Node index, e.g. 1.",
    type=args_validator.validate_node_index
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    _, node = get_network_node(args)
    utils.log(f"NETWORK: {node.network} :: NODE: {node.index} -> bonding account-hash = {node.account.account_hash}")
    utils.log(f"NETWORK: {node.network} :: NODE: {node.index} -> bonding account-id = {node.account.account_id}")
    utils.log(f"NETWORK: {node.network} :: NODE: {node.index} -> bonding private-key = {node.account.private_key}")
    utils.log(f"NETWORK: {node.network} :: NODE: {node.index} -> bonding public-key = {node.account.public_key}")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
