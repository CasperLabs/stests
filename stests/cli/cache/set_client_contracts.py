import argparse

from stests.core import cache
from stests.core import clx
from stests.core.domain import ClientContractType
from stests.core.domain import Network
from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger



# CLI argument parser.
ARGS = argparse.ArgumentParser("Upload a smart contract to stests.")

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
    # Pull.
    network = cache.infra.get_network_by_name(args.network)
    if network is None:
        raise ValueError("Unregistered network.")

    # Set contracts.
    network.client_contracts = []
    set_contract(network, ClientContractType.TRANSFER_U512_STORED, "transfer_to_account")

    # Push.
    cache.infra.set_network(network)

    # Inform.
    logger.log(f"client contracts for network {args.network} were successfully registered")


def set_contract(network: Network, typeof: ClientContractType, name: str):
    """Deploys a client contract to target network.
    
    """
    chash = clx.do_deploy_client_contract(network, typeof, name)
    contract = factory.create_client_contract(network, chash, typeof)
    network.client_contracts.append(contract)


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
