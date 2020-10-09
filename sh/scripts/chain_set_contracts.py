import argparse
import typing

from stests.core import cache
from stests.core import clx
from stests.core import factory
from stests.core.types.chain import Account
from stests.core.types.infra import Network
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env



# CLI argument parser.
ARGS = argparse.ArgumentParser("Uploads smart contracts used in testing to both chain & stests.")

# CLI argument: network name.
ARGS.add_argument(
    "--net",
    default=env.get_network_name(),
    dest="network",
    help="Network name {type}{id}, e.g. nctl1.",
    type=args_validator.validate_network,
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
    if network.faucet is None:
        raise ValueError("Unregistered network faucet.")

    # Set account.
    account = network.faucet

    # Install contracts.
    for contract in clx.contracts.CONTRACTS_BY_HASH:
        _install_contract(network, account, contract)

    # Inform.
    utils.log(f"client contracts for network {args.network} were successfully installed")


def _install_contract(network: Network, account: Account, contract: typing.Callable):
    """Installs a smart contract upon target network.
    
    """
    utils.log(f"{contract.WASM} :: installation starts ... please wait")

    # Dispatch deploy.
    node, deploy_hash, _, _ = contract.install(network, account)
    utils.log(f"{contract.WASM} :: deploy dispatched >- {deploy_hash}")

    # Await deploy processing.
    block_hash = clx.await_deploy_processing(node, deploy_hash)
    utils.log(f"{contract.WASM} :: deploy processed at block {block_hash}")

    # Get named keys.
    keys = clx.contracts.get_named_keys(node, account, block_hash, contract.NKEYS)

    # Persist named keys.
    for key_name, key_hash in keys:
        cache.infra.set_named_key(factory.create_named_key(
            account,
            contract.TYPE,
            key_name,
            key_hash,
        ))
        utils.log(f"{contract.WASM} :: named key -> {key_hash} : {key_name}")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
