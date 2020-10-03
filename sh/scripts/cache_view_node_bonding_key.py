import argparse

from stests.core import cache
from stests.core import factory
from stests.core.types.chain import AccountType
from stests.core.utils import args_validator
from stests.core.utils import cli as utils



# CLI argument parser.
ARGS = argparse.ArgumentParser(f"Displays a node's bonding asymmetric key pair.")

# CLI argument: node reference.
ARGS.add_argument(
    "node",
    help="Node name: {network-type}{network-index}:{node-index}.",
    type=args_validator.validate_node_name
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Unpack.
    network_id = factory.create_network_id(args.node.split(':')[0])
    node_id = factory.create_node_id(network_id, int(args.node.split(':')[-1]))

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
