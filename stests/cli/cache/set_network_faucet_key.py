import argparse

from stests.core import cache
from stests.core.domain import AccountStatus
from stests.core.domain import AccountType
from stests.core.utils import args_validator
from stests.core.utils import crypto
from stests.core.utils import factory
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
    # Set network.
    network_id = factory.create_network(args.network)
    network = cache.get_network(network_id)
    if network is None:
        raise ValueError("Unregistered network.")

    # Set key pair.
    private_key, public_key = crypto.get_key_pair_from_pvk_pem_file(args.pem_path, crypto.KeyEncoding.HEX)

    # Set network's faucet account.
    network.faucet = factory.create_account(
        private_key=private_key,
        public_key=public_key,
        typeof=AccountType.FAUCET,
        status=AccountStatus.ACTIVE,
    )

    # Cache.
    cache.set_network(network)

    logger.log("Network faucet key successfully registered")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
