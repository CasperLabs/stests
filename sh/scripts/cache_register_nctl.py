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
ARGS = argparse.ArgumentParser("Register an nctl network with stests.")

# Map: key prefix to algo.
KEY_ALGO = {
    "01": "ed25519",
    "02": "secp256k1",
}


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    for artefacts in _yield_artefacts():
        _register(artefacts)


def _get_account(accounts, public_key, key_algo):
    """Returns matching entry in accounts.csv.
    
    """
    for key, initial_balance, stake_weight in accounts:
        if key.startswith(f"0{key_algo.value}") and key.endswith(public_key):
            return key, KEY_ALGO[key[0:2]], initial_balance, int(stake_weight)


def _yield_artefacts():
    """Yields aretefacts for mapping to stests types.
    
    """
    # Set path to nctl network artefacts.
    path = pathlib.Path(os.getenv("NCTL")) / "assets"
    if not path.exists() or not path.is_dir():
        raise ValueError(f"Invalid nctl network - network path not found: {path}")

    # Set paths to each network.
    paths = [i for i in path.rglob("net-*") if i.is_dir()]
    if not paths:
        raise ValueError(f"Invalid nctl network - networks undefined")

    # For each nctl network, yield relevant artefacts.
    for path in paths:
        yield int(str(path).split("-")[-1]), \
              _get_artefacts_accounts(path), \
              _get_artefacts_faucet(path), \
              _get_artefacts_nodeset(path)
    

def _get_artefacts(network_idx: int):
    """Returns network artefacts to be mapped.
    
    """
    # Set path to nctl network artefacts.
    path = pathlib.Path(os.getenv("NCTL")) / "assets" / f"net-{network_idx}"
    if not path.exists() or not path.is_dir():
        raise ValueError(f"Invalid nctl network - path not found: {path}")
    
    return \
        _get_artefacts_accounts(path), \
        _get_artefacts_faucet(path), \
        _get_artefacts_nodeset(path)


def _get_artefacts_accounts(path: pathlib.Path) -> typing.List[dict]:
    """Returns accounts artefacts to be mapped.
    
    """
    # Set path to accounts.csv.
    path = path / "chainspec" / "accounts.csv"
    if not path.exists():
        raise ValueError(f"Invalid nctl network - accounts file not found: {path}")
    
    # Open accounts.csv.
    with open(path, 'r') as fstream:
        data = fstream.readlines()

    return [i[0:-1].split(',') for i in data]


def _get_artefacts_faucet(path: pathlib.Path):
    """Returns faucet artefacts to be mapped.
    
    """
    # Set path to private key.
    path = path / "faucet" / "secret_key.pem"
    if not path.exists():
        raise ValueError(f"Invalid nctl network - private key file not found: {path}")
    
    return path


def _get_artefacts_nodeset(path: pathlib.Path):
    """Returns nodeset artefacts to be mapped.
    
    """
    # Set path to nodeset.
    path = path / "nodes"
    if not path.exists():
        raise ValueError(f"Invalid nctl network - nodes undefined")

    # Set paths to each node.
    paths = [i for i in path.rglob("node-*") if i.is_dir()]
    if not paths:
        raise ValueError(f"Invalid nctl network - nodes undefined")
    
    return [_get_artefacts_node(i) for i in paths]


def _get_artefacts_node(path: pathlib.Path) -> typing.Tuple[int, dict, pathlib.Path]:
    """Returns node artefacts to be mapped.
    
    """
    # Set path to config.
    path_cfg = path / "config" / "node-config.toml"
    if not path_cfg.exists():
        raise ValueError(f"Invalid nctl node - node config toml file not found: {path}")
    
    # Set path to private key.
    path_pvk = path / "keys" / "secret_key.pem"
    if not path_pvk.exists():
        raise ValueError(f"Invalid nctl node - private key file not found: {path}")

    return \
        int(str(path).split("-")[-1]), \
        toml.load(path_cfg), \
        path_pvk


def _register(artefacts):
    """Register a network.
    
    """
    # Destructure artefacts.
    network_idx, accounts, faucet_pvk_as_pem, nodeset = artefacts

    network = _register_network(network_idx)
    _register_faucet(network, faucet_pvk_as_pem)
    for node in nodeset:
        _register_node(network, accounts, node)


def _register_faucet(network: Network, path_pvk_pem: str):
    """Register a network's faucet account.
    
    """
    # Set key pair.
    private_key, public_key = crypto.get_key_pair_from_pvk_pem_file(
        path_pvk_pem,
        crypto.DEFAULT_KEY_ALGO,
        crypto.KeyEncoding.HEX
        )

    # Set faucet.
    network.faucet = factory.create_account(
        network=network.name,
        typeof=AccountType.FAUCET,
        index=0,
        key_algo=crypto.DEFAULT_KEY_ALGO,
        private_key=private_key,
        public_key=public_key,
    )

    # Push.
    cache.infra.set_network(network)

    # Inform.
    utils.log(f"Registered {network.name} - faucet key")
    

def _register_network(network_idx: int):
    """Register a network.
    
    """
    # Set network.
    network = factory.create_network(f"nctl{network_idx}", f"casper-net-{network_idx}")

    # Push to cache.
    cache.infra.set_network(network)

    # Inform.
    utils.log(f"Registered {network.name} - metadata")

    return network


def _register_node(network: Network, accounts: dict, info: typing.Tuple[int, dict, pathlib.Path]):
    """Register a network node.
    
    """
    # Destructure node info.
    index, cfg, path_pvk_pem = info

    # Set bonding key pair.
    private_key, public_key = crypto.get_key_pair_from_pvk_pem_file(
        path_pvk_pem,
        crypto.DEFAULT_KEY_ALGO,
        crypto.KeyEncoding.HEX
        )

    # Get staking weight from entry in accounts.csv.
    _, _, _, stake_weight = _get_account(accounts, public_key, crypto.DEFAULT_KEY_ALGO)

    # Destructure node host & port.
    node_address = cfg['http_server']['address']
    node_host = node_address.split(":")[0]
    node_port = int(node_address.split(":")[1])

    # Set node.
    node = factory.create_node(
        host=node_host,
        index=index,  
        network_id=factory.create_network_id(network.name_raw),
        port=node_port,
        typeof=NodeType.FULL if stake_weight > 256 else NodeType.READ_ONLY,
        weight=stake_weight,
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
    utils.log(f"Registered {network.name} - {node.address} : {node.typeof.name}")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
