import argparse

from stests.core import cache
from stests.core.types import Account
from stests.core.types import AccountStatus
from stests.core.types import AccountType
from stests.core.types import KeyPair
from stests.core.types import NetworkIdentifier
from stests.core.types import NodeIdentifier
from stests.core.utils import args_validator
from stests.core.utils import crypto
from stests.core.utils import defaults
from stests.core.utils import logger



# CLI argument parser.
ARGS = argparse.ArgumentParser(f"Register a network's faucet key with stests.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network_name
    )

# Set CLI argument: private key in PEM format.
ARGS.add_argument(
    "pem_path",
    help="Path to the faucet private key in PEM format.",
    type=str
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Unpack arguments.
    network_id = NetworkIdentifier.create(args.network)
    pem_path = args.pem_path

    # Set network.
    network = cache.get_network(network_id)
    if network is None:
        raise ValueError("Unregistered network.")

    # Set network faucet.
    network.faucet = Account.create(
        key_pair=KeyPair.create_from_pvk_pem_file(pem_path),
        network=network_id,
        typeof=AccountType.FAUCET,
        status=AccountStatus.ACTIVE
        )

    # Cache.
    cache.set_network(network)

    logger.log("Network faucet key successfully registered")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
