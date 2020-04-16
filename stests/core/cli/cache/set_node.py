import argparse

from stests.core import cache
from stests.core.domain import NodeType
from stests.core.utils import args_validator
from stests.core.utils import defaults
from stests.core import factory
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
    # Unpack.
    host = args.address.split(':')[0]
    index = int(args.node.split(':')[-1])
    network=args.node.split(':')[0]
    port = int(args.address.split(':')[-1])
    typeof = NodeType[args.typeof.upper()]

    # Instantiate.
    node = factory.create_node(
        host=host,
        index=index,  
        network_id=factory.create_network_id(network),
        port=port,
        typeof=typeof
    )

    # Push.
    cache.infra.set_node(node)

    # Notify.
    logger.log(f"Node {args.node} was successfully registered")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
