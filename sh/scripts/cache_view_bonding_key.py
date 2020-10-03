import argparse

from stests.core import cache
from stests.core import factory
from stests.core.types.chain import AccountType
from stests.core.utils import args_validator
from stests.core.utils import cli as utils



# CLI argument parser.
ARGS = argparse.ArgumentParser(f"Displays a node's bonding asymmetric key pair.")

# CLI argument: network name.
ARGS.add_argument(
    "--net",
    default="nctl1",
    dest="network",
    help="Network name {type}{id}, e.g. nctl1.",
    type=args_validator.validate_network,
    )

# CLI argument: node index.
ARGS.add_argument(
    "--node",
    dest="node",
    help="Node index, e.g. 1.",
    type=args_validator.validate_node_index
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Unpack.
    network_id = factory.create_network_id(args.network)
    node_id = factory.create_node_id(network_id, int(args.node))

    # Pull.
    node = cache.infra.get_node_by_identifier(node_id)
    if node is None:
        utils.log_warning("Unregistered node.")
        return
    if node.account is None:
        utils.log_warning("Unregistered node bonding key.")
        return

    # Inform.
    utils.log(f"NETWORK: {network_id.name} :: NODE: {node.index} -> bonding account-hash = {node.account.account_hash}")
    utils.log(f"NETWORK: {network_id.name} :: NODE: {node.index} -> bonding account-id = {node.account.account_id}")
    utils.log(f"NETWORK: {network_id.name} :: NODE: {node.index} -> bonding private-key = {node.account.private_key}")
    utils.log(f"NETWORK: {network_id.name} :: NODE: {node.index} -> bonding public-key = {node.account.public_key}")

# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
