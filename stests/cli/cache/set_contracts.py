import argparse
import typing

from stests.core import cache
from stests.core import clx
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
    if network.faucet is None:
        raise ValueError("Unregistered network faucet.")

    # Install contracts.
    for contract in clx.CONTRACTS:
        _install_contract(network, contract)

    # Inform.
    logger.log(f"client contracts for network {args.network} were successfully installed")


def _install_contract(network: Network, contract: typing.Callable):
    """Installs a smart contract upon target network.
    
    """
    logger.log(f"{contract.TYPE.value} :: installation starts ... please wait")

    # Dispatch contract to network & await processing.
    contract_hash = clx.install_contract(
        network,
        network.faucet,
        contract,
    )

    # Instantiate domain object.
    contract_info = factory.create_contract(
        network,
        network.faucet,
        contract_hash=contract_hash,
        contract_name=contract.NAME,
        contract_type=contract.TYPE,
        )

    # Update cache.
    cache.infra.set_contract(contract_info)

    logger.log(f"{contract.TYPE.value} :: installed -> contract-hash={contract_hash}")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
