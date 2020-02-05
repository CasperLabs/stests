import argparse

from stests.core import cache
from stests.core.types import Account
from stests.core.types import AccountStatus
from stests.core.types import AccountType
from stests.core.types import KeyPair
from stests.core.types import NetworkIdentifier
from stests.core.types import NodeIdentifier
from stests.core.utils import args_validator
from stests.core.utils import args_validator
from stests.core.utils import crypto
from stests.core.utils import defaults
from stests.core.utils import logger



# CLI argument parser.
ARGS = argparse.ArgumentParser(f"Register a node's bonding key with stests.")

# CLI argument: node reference.
ARGS.add_argument(
    "node",
    help="Node name: {network-type}{network-index}:{node-index}.",
    type=args_validator.validate_node_name
    )

# Set CLI argument: private key in PEM format.
ARGS.add_argument(
    "pem_path",
    help="Path to the node's private key in PEM format.",
    type=str
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Unpack arguments.
    network_name = args.node.split(':')[0]
    node_index = int(args.node.split(':')[-1])
    pem_path = args.pem_path

    # Set identifiers.
    network_id = NetworkIdentifier.create(network_name)
    node_id = NodeIdentifier.create(network_name, node_index)

    # Set network.
    network = cache.get_network(network_id)
    if network is None:
        raise ValueError("Unregistered network.")

    # Set node.
    node = cache.get_node(node_id)
    if node is None:
        raise ValueError("Unregistered node.")

    # Set node account.
    node.account = Account.create(
        key_pair=KeyPair.create_from_pvk_pem_file(args.pem_path),
        network=network_id,
        typeof=AccountType.BOND,
        status=AccountStatus.ACTIVE
        )

    # Cache.
    cache.set_node(node)

    logger.log("Node bonding key successfully registered")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
