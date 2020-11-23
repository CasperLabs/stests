import argparse
import pathlib

from stests.core import cache
from stests.core import crypto
from stests.core import factory
from stests.core.types.chain import AccountType
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env



# CLI argument parser.
ARGS = argparse.ArgumentParser(f"Register a network's faucet key with stests.")

# CLI argument: network name.
ARGS.add_argument(
    "--net",
    default=env.get_network_name(),
    dest="network",
    help="Network name {type}{id}, e.g. nctl1.",
    type=args_validator.validate_network,
    )

# CLI argument: faucet secret key PEM file path.
ARGS.add_argument(
    "--path",
    dest="pem_path",
    help="Absolute path to the faucet secret key in PEM format.",
    type=args_validator.validate_filepath,
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """    
    # Pull.
    network_id = factory.create_network_id(args.network)
    network = cache.infra.get_network(network_id)
    if network is None:
        raise ValueError("Unregistered network.")

    # Set key pair.
    pvk, pbk = crypto.get_key_pair_from_pvk_pem_file(
        args.pem_path,
        crypto.KeyAlgorithm.ED25519,
        crypto.KeyEncoding.HEX,
        )

    # Set faucet.
    network.faucet = factory.create_account(
        network=network.name,
        typeof=AccountType.NETWORK_FAUCET,
        index=0,
        key_algo=crypto.KeyAlgorithm.ED25519,
        private_key=pvk,
        public_key=pbk,
    )

    # Push.
    cache.infra.set_network(network)

    # Inform.
    utils.log(f"Network {args.network} faucet key was successfully registered")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
