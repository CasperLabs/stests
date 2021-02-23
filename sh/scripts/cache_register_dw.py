import argparse
import os
import pathlib
import random
import typing

import toml

from stests.core import cache
from stests.core import crypto
from stests.core import factory
from stests.core.types.chain import AccountType
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.types.infra import NodeGroup
from stests.core.types.infra import NodeType
from stests.core.utils import cli as utils



# CLI argument parser.
ARGS = argparse.ArgumentParser("Register an DW network with stests.")

# CLI argument: node index.
ARGS.add_argument(
    "--assets",
    dest="assets",
    help="Folder within which assets have been laid out.",
    type=str
    )

# Map: key prefix to algo.
KEY_ALGO = {
    "01": "ed25519",
    "02": "secp256k1",
}


def main(args):
    """Entry point.

    :param args: Parsed CLI arguments.

    """
    chainspec, accounts, path_to_faucet_pvk, nodeset = _get_artefacts(args)
    network = _register_network(chainspec, 1, 1, len(nodeset), path_to_faucet_pvk)
    for idx, info in enumerate(nodeset):
        _register_node(network, accounts, idx, info)


def _get_artefacts(args):
    """Yields aretefacts for mapping to stests types.

    """
    path = pathlib.Path(args.assets)
    if not path.exists() or not path.is_dir():
        raise ValueError(f"Invalid dw network - assets path not found: {path}")

    path_to_assets = sorted([pathlib.Path(f.path) for f in os.scandir(path) if f.is_dir()])
    path_to_chainspec = path_to_assets[0] / "etc" / "casper" / "1_0_0" / "chainspec.toml"
    path_to_accounts_toml = path_to_assets[0] / "etc" / "casper" / "1_0_0" / "accounts.toml"
    path_to_faucet_pvk = path_to_assets[0] / "etc" / "casper" / "keys" / "faucet" / "secret_key.pem"

    return \
        _get_artefacts_chainspec(path_to_chainspec), \
        _get_artefacts_accounts(path_to_accounts_toml), \
        path_to_faucet_pvk, \
        [_get_artefacts_node(i) for i in path_to_assets]


def _get_artefacts_accounts(path: pathlib.Path) -> typing.List[dict]:
    """Returns accounts artefacts to be mapped.

    """
    if not path.exists():
        raise ValueError(f"Invalid network - accounts file not found: {path}")

    return toml.load(path)


def _get_artefacts_chainspec(path: pathlib.Path) -> typing.List[dict]:
    """Returns chainspec artefacts to be mapped.

    """
    if not path.exists():
        raise ValueError(f"Invalid network - chainspec file not found: {path}")

    return toml.load(path)


def _get_artefacts_node(path: pathlib.Path) -> typing.Tuple[int, dict, pathlib.Path]:
    """Returns node artefacts to be mapped.

    """
    # Set path to config.
    path_cfg = path / "etc" / "casper" / "1_0_0" / "config.toml"
    if not path_cfg.exists():
        raise ValueError(f"Invalid node - node config toml file not found: {path}")

    # Set path to private key.
    path_pvk = path / "etc" / "casper" / "keys" / "secret_key.pem"
    if not path_pvk.exists():
        raise ValueError(f"Invalid nctl node - private key file not found: {path}")

    # Set config.
    cfg = toml.load(path_cfg)

    # Set is bootstrap flag.
    is_bootstrap = cfg["network"]["public_address"] in cfg["network"]["known_addresses"]

    return \
        str(path).split('/')[-1], \
        cfg, \
        path_pvk, \
        is_bootstrap


def _register_network(
    chainspec: dict,
    network_idx: int,
    count_of_bootstrap_nodes: int,
    count_of_genesis_nodes: int,
    path_to_faucet_pvk: pathlib.Path
    ):
    """Register a network.

    """
    # Set network.
    network = factory.create_network(
        f"lrt{network_idx}",
        chainspec['network']['name'],
        count_of_bootstrap_nodes,
        count_of_genesis_nodes,
        )

    # Set faucet.
    private_key, public_key = crypto.get_key_pair_from_pvk_pem_file(
        path_to_faucet_pvk,
        crypto.DEFAULT_KEY_ALGO,
        crypto.KeyEncoding.HEX
        )
    network.faucet = factory.create_account(
        network=network.name,
        typeof=AccountType.NETWORK_FAUCET,
        index=0,
        key_algo=crypto.DEFAULT_KEY_ALGO,
        private_key=private_key,
        public_key=public_key,
    )

    # Push to cache.
    cache.infra.set_network(network)
    utils.log(f"registered network")

    return network


def _register_node(
    network: Network,
    accounts: dict,
    index: int,
    info: typing.Tuple[str, dict, pathlib.Path]):
    """Register a network node.

    """
    host, cfg, path_to_pvk, is_boostrap = info

    # Set bonding key pair.
    private_key, public_key = crypto.get_key_pair_from_pvk_pem_file(
        path_to_pvk,
        crypto.DEFAULT_KEY_ALGO,
        crypto.KeyEncoding.HEX
        )

    # Set staking weight.
    _, _, _, stake_weight = _get_account(accounts, public_key, crypto.DEFAULT_KEY_ALGO)

    # Set group.
    group = NodeGroup.BOOTSTRAP if is_boostrap else NodeGroup.GENESIS

    # Set node.
    node = factory.create_node(
        group=group,
        host=host,
        index=index,
        network_id=factory.create_network_id(network.name_raw),
        port_rest=8888,
        port_rpc=7777,
        port_event=9999,
        typeof=NodeType.VALIDATOR,
        use_to_dispatch=True,
        use_to_monitor=random.choice(range(4)) == 0,
        use_to_query=True,
        weight=stake_weight,
    )

    # Set bonding account.
    node.account = factory.create_account(
        network=network.name,
        typeof=AccountType.VALIDATOR_BOND,
        index=index,
        key_algo=crypto.KeyAlgorithm.ED25519,
        private_key=private_key,
        public_key=public_key,
    )

    # Push.
    cache.infra.set_node(node)
    utils.log(f"Registered {node.label}")


def _get_account(accounts, public_key, key_algo):
    """Returns matching entry in accounts.toml.

    """

    for account in accounts["accounts"]:
        key = account["public_key"]
        initial_balance = account["balance"]
        stake_weight = account["bonded_amount"]
        if key.startswith(f"0{key_algo.value}") and key.endswith(public_key):
            return key, KEY_ALGO[key[0:2]], initial_balance, int(stake_weight)


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
