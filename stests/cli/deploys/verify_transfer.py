import argparse
import random

from casperlabs_client import CasperLabsClient

from stests.core import cache
from stests.core.clx.defaults import CLX_TX_FEE
from stests.core.clx.defaults import CLX_TX_GAS_PRICE
from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger


# CLI argument parser.
ARGS = argparse.ArgumentParser("Verifies that deploys can be dispatched to a network.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Set network.
    network_id=factory.create_network_id(args.network)
    network = cache.infra.get_network(network_id)
    if network is None:
        raise ValueError("Unregistered network.")
    if network.faucet is None:
        raise ValueError("Unregistered network faucet.")

    # Set node.
    nodes = cache.infra.get_nodes(network_id)
    if not nodes:
        raise ValueError("Unregistered nodes.")
    node = random.choice(nodes)

    # Set counter-parties.
    cp1 = network.faucet
    cp2 = node.account

    # Perform transfer.
    client = CasperLabsClient(host=node.host, port=node.port)
    dhash = client.transfer(
        amount=int(1e8),
        target_account_hex=cp2.public_key,
        from_addr=cp1.public_key,
        private_key=cp1.private_key_as_pem_filepath,
        # TODO: allow these to be passed in via standard arguments
        payment_amount=CLX_TX_FEE,
        gas_price=CLX_TX_GAS_PRICE
    )

    dinfo = client.showDeploy(dhash, wait_for_processed=False)
    print(f"transfer status (immediate): {dinfo.status}")

    dinfo = client.showDeploy(dhash, wait_for_processed=True)
    print(f"transfer status (processed): {dinfo.status}")



# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
