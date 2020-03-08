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
    # Unpack.
    network_id = factory.create_network_id(args.node.split(':')[0])
    node_id = factory.create_node_id(network_id, int(args.node.split(':')[-1]))

    # Pull.
    node = cache.infra.get_node(node_id)
    if node is None:
        raise ValueError("Unregistered node.")

    # Set key pair.
    pvk, pbk = crypto.get_key_pair_from_pvk_pem_file(args.pem_path, crypto.KeyEncoding.HEX)

    # Set bonding account.
    node.account = factory.create_account(
        index=-node_id.index,
        private_key=pvk,
        public_key=pbk,
        status=AccountStatus.ACTIVE,
        typeof=AccountType.BOND
    )

    # Push.
    cache.infra.set_node(node)

    # Inform.
    logger.log(f"Node {args.node} bonding key was successfully registered")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
