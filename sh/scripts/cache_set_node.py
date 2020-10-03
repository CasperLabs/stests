import argparse

from stests.core import cache
from stests.core import factory
from stests.core.types.infra import NodeType
from stests.core.utils import args_validator
from stests.core.utils import cli as utils


# CLI argument parser.
ARGS = argparse.ArgumentParser(f"Upload node information to stests.")

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

# Set CLI argument: node address.
ARGS.add_argument(
    "--address",
    default="localhost",
    dest="address",
    help="Node public network address: {host}:{port}.",
    type=args_validator.validate_node_address
    )

# Set CLI argument: node type.
ARGS.add_argument(
    "--type",
    choices=[i.name.lower() for i in NodeType],
    dest="typeof",
    help="Node type.",
    type=str
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Unpack.
    host = args.address.split(':')[0]
    index = int(args.node)
    network = args.network
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
    utils.log(f"Node {args.network}:{args.node} was successfully registered")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
