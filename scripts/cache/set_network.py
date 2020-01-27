import argparse
import json

from stests.core.cache.factory import get_store
from stests.core.types import Network
from stests.core.types import NetworkLifetime
from stests.core.types import NetworkOperatorType
from stests.core.utils import defaults
from stests.core.utils import encoder



# Set CLI argument parser.
ARGS = argparse.ArgumentParser(
    f"Uploads network information to stests cache."
)

# Set CLI argument: network identifer.
ARGS.add_argument(
    "--network-id",
    help="Identifier of network being tested.",
    dest="network_id",
    type=str,
    default=defaults.NETWORK_ID
    )

# Set CLI argument: network lifetime.
ARGS.add_argument(
    "--lifetime",
    help="Estimated lifetime of network being tested.",
    dest="lifetime",
    type=str,
    default="REPEAT"
    )

# Set CLI argument: network operator type.
ARGS.add_argument(
    "--operator-type",
    help="Type of network operator.",
    dest="operator_type",
    type=str,
    default="LOCAL"
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    network = get_network(args)
    with get_store(network.name) as store:
        store.delete(
            get_cache_key(network)
        )
        store.set(
            get_cache_key(network),
            get_cache_data(network)
        )


def get_network(args):
    """Returns domain object instance deserialised from CLI args.
    
    """
    network = Network(args.network_id.upper(), [])
    network.metadata.lifetime = NetworkLifetime[args.lifetime]
    network.metadata.operator_type = NetworkOperatorType[args.operator_type]

    return network


def get_cache_key(network):
    """Returns cache key to use.
    
    """
    return f"{network.name}"


def get_cache_data(network):
    """Returns cache data to persist in cache.
    
    """
    return json.dumps(encoder.encode(network), indent=4)


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
