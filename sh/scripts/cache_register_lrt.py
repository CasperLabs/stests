import argparse
import os
import pathlib
import typing

import toml

from stests.core import cache
from stests.core import crypto
from stests.core import factory
from stests.core.types.chain import AccountType
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.types.infra import NodeType
from stests.core.utils import cli as utils



# CLI argument parser.
ARGS = argparse.ArgumentParser("Register an LRT network with stests.")


def main(args):
    """Entry point.

    :param args: Parsed CLI arguments.

    """
    for network_id, chain_name, faucet, nodeset in _yield_assets():
        # Register network.
        network = _register_network(network_id, chain_name)

        # Register faucet.
        _register_faucet(network, faucet)

        # Register nodeset.
        for index, info in enumerate(nodeset, start=1):
            _register_node(network, index, info)


def _yield_assets() -> typing.Tuple[str, typing.List, typing.List]:
    """Yields relevant assets from each sub-directory within $HOME/.casperlabs-stests/nets.

    """
    path = pathlib.Path(os.path.expanduser("~/.casperlabs-stests/nets"))
    if not path.exists or not path.is_dir:
        raise ValueError(f"Invalid network metadata directory: {path}")

    for network_id in os.listdir(path):
        path_assets = path / network_id
        yield \
            network_id, \
            _get_chain_name(path_assets), \
            _get_faucet(path_assets), \
            _get_nodeset(path_assets)


def _get_chain_name(path_assets: pathlib.Path) -> str:
    """Returns chain name as specified within chainspec.

    """
    chainspec = _get_chainspec(path_assets)

    return chainspec['genesis']['name']


def _get_chainspec(path_assets: pathlib.Path) -> str:
    """Returns decoded chainspec.

    """
    path_chainspec = path_assets / "chainspec.toml"
    if not path_chainspec.exists():
        raise ValueError(f"chainspec.toml file not found: {path_chainspec}")

    return toml.load(path_chainspec)


def _get_faucet(path_assets: pathlib.Path) -> typing.Tuple[str, crypto.KeyAlgorithm]:
    """Returns faucet information.

    """
    path_sk_pem = path_assets / "faucet" / "secret_key.pem"
    if not path_sk_pem.exists():
        raise ValueError(f"faucet secret_key.pem file not found: {path_sk_pem}")

    return (path_sk_pem, crypto.KeyAlgorithm.ED25519)


def _get_nodeset(path_assets: pathlib.Path) -> typing.List[typing.Tuple[str, int, int, str]]:
    """Returns nodeset information.

    """
    # Read node.csv.
    path = path_assets / "nodes.csv"
    if not path.exists:
        raise ValueError(f"nodes.csv file not found: {path}")
    with open(path, 'r') as fstream:
        data = fstream.readlines()

    return [_get_node(path_assets, i.split(",")) for i in data]


def _get_node(path_assets: pathlib.Path, info):
    """Returns node information.

    """
    host, port, _, weight = info

    # Set path to secret key.
    path_sk_pem = path_assets / "configs" / host / "secret_key.pem"
    if not path_sk_pem.exists():
        raise ValueError(f"node secret_key.pem file not found: {path_sk_pem}")

    return (host, int(port), int(weight), path_sk_pem)


def _register_network(network_id: str, chain_name: str):
    """Register a network.

    """
    network = factory.create_network(network_id, chain_name)
    cache.infra.set_network(network)

    # Inform.
    utils.log(f"registered {network.name_raw} - metadata")

    return network


def _register_faucet(network: Network, info: typing.Tuple[str, crypto.KeyAlgorithm]):
    """Register a network's faucet account.

    """
    # Set key pair.
    path_secret_key_pem, secret_key_algo = info
    private_key, public_key = \
        crypto.get_key_pair_from_pvk_pem_file(path_secret_key_pem, algo=secret_key_algo, encoding=crypto.KeyEncoding.HEX)

    # Set faucet.
    network.faucet = factory.create_account(
        network=network.name,
        typeof=AccountType.FAUCET,
        index=0,
        key_algo=crypto.KeyAlgorithm.ED25519,
        private_key=private_key,
        public_key=public_key,
    )

    # Push.
    cache.infra.set_network(network)

    # Inform.
    utils.log(f"registered {network.name_raw} - faucet key")


def _register_node(
    network: Network,
    index: int,
    info: typing.Tuple[str, int, int, pathlib.Path]
    ):
    """Register a network node.

    """
    # Destructure node info.
    host, port, weight, path_sk_pem = info

    # Set node.
    node = factory.create_node(
        host=host,
        index=index,
        network_id=factory.create_network_id(network.name_raw),
        port=port,
        typeof=NodeType.FULL if weight > 1000 else NodeType.READ_ONLY,
        weight=weight,
    )

    # Set bonding key pair.
    private_key, public_key = crypto.get_key_pair_from_pvk_pem_file(
        path_sk_pem,
        algo=crypto.KeyAlgorithm.ED25519,
        encoding=crypto.KeyEncoding.HEX,
        )

    # Set bonding account.
    node.account = factory.create_account(
        network=network.name,
        typeof=AccountType.BOND,
        index=index,
        key_algo=crypto.KeyAlgorithm.ED25519,
        private_key=private_key,
        public_key=public_key,
    )

    # Push.
    cache.infra.set_node(node)

    # Inform.
    utils.log(f"registered {network.name_raw} - {node.address_rpc} : {node.typeof.name}")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
