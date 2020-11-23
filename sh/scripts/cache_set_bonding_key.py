import argparse

from stests.core import cache
from stests.core import crypto
from stests.core import factory
from stests.core.types.chain import AccountType
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env


# CLI argument parser.
ARGS = argparse.ArgumentParser(f"Register a node's bonding key with stests.")

# CLI argument: network name.
ARGS.add_argument(
    "--net",
    default=env.get_network_name(),
    dest="network",
    help="Network name {type}{id}, e.g. nctl1.",
    type=args_validator.validate_network,
    )

# CLI argument: node index.
ARGS.add_argument(
    "--node",
    dest="node",
    help="Node index, e.g. 1.",
    type=args_validator.validate_node_index
    )

# CLI argument: faucet secret key PEM file path.
ARGS.add_argument(
    "--path",
    dest="pem_path",
    help="Absolute path to the node's secret key in PEM format.",
    type=args_validator.validate_filepath,
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Unpack.
    network_id = factory.create_network_id(args.network)
    node_id = factory.create_node_id(network_id, int(args.node))

    # Pull.
    node = cache.infra.get_node(node_id)
    if node is None:
        raise ValueError("Unregistered node.")

    # Set key pair.
    pvk, pbk = crypto.get_key_pair_from_pvk_pem_file(
        args.pem_path,
        algo=crypto.KeyAlgorithm.ED25519,
        encoding=crypto.KeyEncoding.HEX
        )

    # Set bonding account.
    node.account = factory.create_account(
        network=network_id.name,
        typeof=AccountType.VALIDATOR_BOND,
        index=-node_id.index,
        key_algo=crypto.KeyAlgorithm.ED25519,
        private_key=pvk,
        public_key=pbk,
    )

    # Push.
    cache.infra.set_node(node)

    # Inform.
    utils.log(f"Node {args.network}:{args.node} bonding key was successfully registered")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
