import argparse
import json

from stests.core.cache.factory import get_store
from stests.core.types import Network
from stests.core.types import Node
from stests.core.types import NodeType
from stests.core.utils import defaults
from stests.core.utils import encoder



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
    help="Node type, i.e. full | readonly.",
    dest="typeof",
    type=str,
    default=defaults.NODE_TYPE
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    node = get_node(args)
    network = get_network(args)

    print(network)


def get_node(args):
    """Returns domain object instance deserialised from CLI args.
    
    """
    node = Node()
    # return Node(
    #     defaults.NODE_HOST,
    #     defaults.NODE_PORT,
    #     defaults.NETWORK_ID,
    #     Account.create(AccountType.VALIDATOR)
    #     )
            
    #             node = Node(args.network_id.upper(), [])
    # node.metadata.typeof = NodeType[args.typeof]

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
