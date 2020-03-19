import argparse

from stests.core import cache
from stests.core import clx
from stests.core.domain import Network
from stests.core.domain import NetworkContractType
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
    if network.faucet is None:
        raise ValueError("Unregistered network faucet.")

    # Set contracts.
    set_contract(network, NetworkContractType.TRANSFER_U512_STORED, "transfer_to_account")

    # Inform.
    logger.log(f"client contracts for network {args.network} were successfully registered")


def set_contract(network: Network, typeof: NetworkContractType, name: str):
    """Deploys a client contract to target network.
    
    """
    # Dispatch contract to network & await processing.
    chash = clx.do_deploy_client_contract(network, typeof, name)

    # Instantiate domain object.
    contract = factory.create_client_contract(network, chash, typeof)

    # Persist within cache.
    cache.infra.set_client_contract(contract)


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
