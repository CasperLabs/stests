import argparse

from scripts.cache import utils
from stests.core import cache
from stests.core.types import Network
from stests.core.types import NetworkType
from stests.core.types import Node
from stests.core.types import NodeType
from stests.core.utils import defaults



# CLI argument parser.
ARGS = argparse.ArgumentParser(f"Upload node information to stests.")

# CLI argument: network type.
ARGS.add_argument(
    "network_type",
    choices=[i.name.lower() for i in NetworkType],
    help="Type of network being tested.",
    type=str
    )

# CLI argument: network index.
ARGS.add_argument(
    "network_idx",
    help="Network index - must be between 1 and 99.",
    type=utils.validate_network_idx
    )

# CLI argument: network index.
ARGS.add_argument(
    "node_idx",
    help="Node index - must be between 1 and 999.",
    type=utils.validate_node_idx
    )

# Set CLI argument: node host.
ARGS.add_argument(
    "host",
    default=defaults.NODE_HOST,
    help="Node host.",
    type=str
    )

# Set CLI argument: node port.
ARGS.add_argument(
    "port",
    default=defaults.NODE_PORT,
    help="Node public GRPC port.",
    type=int
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
    cache.set_node(Node(
        host=args.host,
        idx=args.node_idx,  
        network_idx=args.network_idx,
        network_type=NetworkType[args.network_type.upper()],      
        typeof = NodeType[args.typeof.upper()]
    ))    


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
