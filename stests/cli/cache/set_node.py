import argparse

from stests.core import cache
from stests.core.types import Network
from stests.core.types import NetworkType
from stests.core.types import Node
from stests.core.types import NodeType
from stests.core.utils import args_validator
from stests.core.utils import defaults
from stests.core.utils import logger



# CLI argument parser.
ARGS = argparse.ArgumentParser(f"Upload node information to stests.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network_name
    )
    
# CLI argument: network index.
ARGS.add_argument(
    "index",
    help="Node index - must be between 1 and 999.",
    type=args_validator.validate_node_index
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
    type=args_validator.validate_node_port
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
    instance = Node.create(
        host=args.host,
        index=args.index,  
        network=args.network,
        port=args.port,
        typeof = NodeType[args.typeof.upper()]
    )
    cache.set_node(instance)    
    logger.log("Node information successfully registered")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
