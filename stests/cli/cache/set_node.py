import argparse

from stests.core import cache
from stests.core.types import Network
from stests.core.types import NetworkType
from stests.core.types import Node
from stests.core.types import NetworkIdentifier
from stests.core.types import NodeType
from stests.core.utils import args_validator
from stests.core.utils import defaults
from stests.core.utils import logger



# CLI argument parser.
ARGS = argparse.ArgumentParser(f"Upload node information to stests.")

# CLI argument: node reference.
ARGS.add_argument(
    "node",
    help="Node name: {network-type}{network-index}:{node-index}.",
    type=args_validator.validate_node_name
    )

# Set CLI argument: node host.
ARGS.add_argument(
    "address",
    default=defaults.NODE_HOST,
    help="Node public network address: {host}:{port}.",
    type=args_validator.validate_node_address
    )

# Set CLI argument: node type.
ARGS.add_argument(
    "typeof",
    choices=[i.name.lower() for i in NodeType],
    help="Node type.",
    type=str
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Unpack arguments.
    host = args.address.split(':')[0]
    index = int(args.node.split(':')[-1])
    network=NetworkIdentifier.create(args.node.split(':')[0])
    port = int(args.address.split(':')[-1])
    typeof = NodeType[args.typeof.upper()]

    # Instantiate.
    node = Node.create(
        host=host,
        index=index,  
        network=network,
        port=port,
        typeof=typeof
    )
    
    # Encache.
    cache.set_node(node)    

    logger.log("Node information successfully registered")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
