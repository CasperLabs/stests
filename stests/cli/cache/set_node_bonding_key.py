import argparse

from stests.core import cache
from stests.core.domain import AccountStatus
from stests.core.domain import AccountType
from stests.core.utils import args_validator
from stests.core.utils import crypto
from stests.core.utils import factory
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
    # Set network.
    network_name = args.node.split(':')[0]
    network_id = factory.create_network_identifier(network_name)
    network = cache.get_network(network_id)
    if network is None:
        raise ValueError("Unregistered network.")

    # Set node.
    node_index = int(args.node.split(':')[-1])
    node_id = factory.create_node_identifier(network_id, node_index)
    node = cache.get_node(node_id)
    if node is None:
        raise ValueError("Unregistered node.")

    # Set key pair.
    private_key, public_key = crypto.get_key_pair_from_pvk_pem_file(args.pem_path, crypto.KeyEncoding.HEX)

    # Set node's bonding account.
    node.account = factory.create_account(
        private_key=private_key,
        public_key=public_key,
        status=AccountStatus.ACTIVE,
        typeof=AccountType.BOND
    )

    # Cache.
    cache.set_node(node)

    logger.log("Node bonding key successfully registered")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
