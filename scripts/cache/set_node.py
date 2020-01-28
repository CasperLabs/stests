import argparse

from stests.core import cache
from stests.core.types import Network
from stests.core.types import NetworkLifetime
from stests.core.types import NetworkOperatorType
from stests.core.types import Node
from stests.core.types import NodeType
from stests.core.utils import defaults


# Set CLI argument parser.
ARGS = argparse.ArgumentParser(
    f"Uploads node information to stests cache."
)

# Set CLI argument: network identifer.
ARGS.add_argument(
    "--network-id",
    help="Identifier of network being tested.",
    dest="network_id",
    type=str,
    default=defaults.NETWORK_ID
    )

# Set CLI argument: node identifer.
ARGS.add_argument(
    "--name",
    help="Name of node being tested.",
    dest="name",
    type=str,
    default=defaults.NODE_NAME
    )

# Set CLI argument: node host.
ARGS.add_argument(
    "--host",
    help="Node's host.",
    dest="host",
    type=str,
    default=defaults.NODE_HOST
    )

# Set CLI argument: node port.
ARGS.add_argument(
    "--port",
    help="Node's public GRPC port.",
    dest="port",
    type=str,
    default=defaults.NODE_PORT
    )

# Set CLI argument: node type.
ARGS.add_argument(
    "--typeof",
    help="Node type, i.e. FULL | READONLY.",
    dest="typeof",
    type=str,
    default=defaults.NODE_TYPE
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    network = cache.get_network(args.network_id)
    network.nodeset = [n for n in network.nodeset if n.name != args.name] + \
                      [get_node(args)]
    cache.set_network(network)


def get_node(args):
    """Returns domain object instance deserialised from CLI args.
    
    """
    node = Node()
    node.host = args.host
    node.port = args.port
    node.name = args.name
    node.network_id = args.network_id
    node.metadata.typeof = args.typeof

    return node


def get_network(args):
    """Pulls network information from cache.
    
    """
    with get_store(args.network_id) as store:
        return store.get(
            args.network_id
        )


def get_network_cache_key(network):
    """Returns cache key to use.
    
    """
    return f"{network.name}"


def get_network_cache_data(network):
    """Returns cache data to persist in cache.
    
    """
    return json.dumps(encoder.encode(network), indent=4)


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
