import argparse

from stests.core import cache
from stests.core.types import Network
from stests.core.types import NetworkLifetime
from stests.core.types import NetworkOperatorType
from stests.core.utils import defaults



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
    cache.set_network(get_network(args))


def get_network(args):
    """Returns domain object instance deserialised from CLI args.
    
    """
    network = Network(args.network_id.upper(), [])
    network.metadata.lifetime = NetworkLifetime[args.lifetime]
    network.metadata.operator_type = NetworkOperatorType[args.operator_type]

    return network


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
