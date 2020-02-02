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

# Set CLI argument: Node identifer.
ARGS.add_argument(
    "--node-index",
    help="Identifier of node being tested.",
    dest="node_index",
    type=str,
    default=defaults.NODE_ID
    )

# Set CLI argument: Node's private key PEM file.
ARGS.add_argument(
    "--private-key-pem-file",
    help="The node's private key PEM file.",
    dest="pvk_pem_fpath",
    type=str
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    cache.set_node(get_node(args))


def get_node(args):
    """Returns domain object instance deserialised from CLI args.
    
    """
    node = Node()
    node.host = args.host
    node.name = args.name
    node.network_id = args.network_id
    node.port = args.port
    node.typeof = NodeType[args.typeof]

    return node


def get_network(args):
    """Pulls network information from cache.
    
    """
    with get_store() as store:
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
