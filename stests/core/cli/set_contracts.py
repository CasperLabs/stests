import argparse
import typing

from stests.core import cache
from stests.core import clx
from stests.core.types.chain import Account
from stests.core.types.infra import Network
from stests.core.utils import args_validator
from stests.core import factory
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

    # Set account.
    account = network.faucet

    # Install contracts.
    for contract in clx.contracts.CONTRACTS_BY_HASH:
        _install_contract(network, account, contract)

    # Inform.
    logger.log(f"client contracts for network {args.network} were successfully installed")


def _install_contract(network: Network, account: Account, contract: typing.Callable):
    """Installs a smart contract upon target network.
    
    """
    logger.log(f"{contract.WASM} :: installation starts ... please wait")

    # Install contract under network faucet account.
    _, _, keys = contract.install(network, account)

    # Persist named keys.
    for key_name, key_hash in keys:
        key = factory.create_account_named_key(
            account,
            contract.TYPE,
            key_name,
            network.name,
            key_hash,
        )
        cache.infra.set_account_named_key(key)

    logger.log(f"{contract.WASM} :: installed")
    for key_name, key_hash in keys:
        logger.log(f"{contract.WASM} :: named key -> {key_hash} : {key_name}")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
