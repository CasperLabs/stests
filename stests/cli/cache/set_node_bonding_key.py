import argparse

from stests.core import cache
from stests.core.types import Network
from stests.core.types import NetworkType
from stests.core.types import Node
from stests.core.types import NodeType
from stests.core.utils import args_validator
from stests.core.utils import defaults
from stests.core.utils import logger


from stests.core.types import Account
from stests.core.types import AccountType
from stests.core.types import NetworkIdentifier
from stests.core.types import NodeIdentifier
from stests.core.utils import crypto


# CLI argument parser.
ARGS = argparse.ArgumentParser(f"Upload node bonding provate key to stests.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network_name
    )
    
# CLI argument: node index.
ARGS.add_argument(
    "index",
    help="Node index - must be between 1 and 999.",
    type=args_validator.validate_node_index
    )

# Set CLI argument: private key in PEM format.
ARGS.add_argument(
    "pem_path",
    default=defaults.NODE_HOST,
    help="Path to the node's private key in PEM format.",
    type=str
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Set identifiers.
    network_id = NetworkIdentifier.create(args.network)
    node_id = NodeIdentifier.create(args.network, args.index)

    # Set network.
    network = cache.get_network(network_id)
    if network is None:
        raise ValueError("Unregistered network.")

    # Set node.
    node = cache.get_node(node_id)
    if node is None:
        raise ValueError("Unregistered node.")

    # Set account.
    pvk_hex = crypto.get_pvk_hex_from_pem_file(args.pem_path)

    

    print(pvk_hex)

    AccountType.BOND

    logger.log("Node bonding key successfully registered")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
